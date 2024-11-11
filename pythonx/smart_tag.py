"""
" HACK to make this file source'able by vim as well as importable by Python:
if has('python3')
  py3 from importlib import reload; reload(smart_tag)
else
  py reload(smart_tag)
endif
finish
"""
import os
import vim


class SmartTagFinder(object):

    def __init__(self, verbose=0):
        self.verbose = verbose
        self.cache = {}

    def debug(self, message):
        if self.verbose > 0:
            print(message)

    def command(self, cmd):
        self.debug(cmd)
        vim.command(cmd)

    def get_tags(self, name):
        """Return all tags for name"""
        try:
            return self.cache[name]
        except KeyError:
            self.cache[name] = tags = vim.eval('taglist("^%s$")' % name)
            self.debug("Got %d tags for %s" % (len(tags), name))
            return tags

    @staticmethod
    def filter_class(tags, class_):
        """Return tags that belong to a class."""
        return [t for t in tags if t.get("class") == class_]

    @staticmethod
    def filter_toplevel(tags):
        """Return tags that belong to top-level names."""
        return [t for t in tags if not t.get("class") and t.get('kind') != 'x']

    @staticmethod
    def filter_file(tags, filename):
        """Return tags that are in files/directories with a certain name."""
        return [t for t in tags if os.path.splitext(t.get("filename"))[0].endswith(filename)]

    def priority(self, tag):
        """Compute the priority of a tag (lower is preferred)."""
        filename = tag.get('filename') or ''
        # apply some heuristics; these should be made configurable!
        if 'test' in filename or 'fixture' in filename:
            self.debug('%s looks like a test file, deprioritizing the tag' % filename)
            return 10
        return 0

    def prioritize(self, tags):
        """Reorder tags into priority order."""
        return sorted(tags, key=self.priority)

    def find_best_tag(self, query):
        bits = query.split('.')
        name = bits.pop()
        possibilities = [
            # [[package.]module.]name -> expect name in package/module.py outside class
            (bits, None, name),
        ]
        if bits:
            # [[package.]module.]class.name -> expect name in package/module.py, in a class
            possibilities.append((bits[:-1], bits[-1], name))
        possibilities += [
            # [package] -> expect __init__.py in package/name/__init__.py
            (bits + [name, '__init__'], None, '__init__.py'),
            # [package.]module -> expect name.py in package/name.py
            (bits + [name], None, name + '.py'),
        ]

        for filename_bits, class_, name in possibilities:
            tags = original = self.get_tags(name)
            if not tags:
                continue
            if class_:
                tags = self.filter_class(tags, class_)
                self.debug("%d tags matched class %s" % (len(tags), class_))
            else:
                tags = self.filter_toplevel(tags)
                self.debug("%d tags are top-level" % (len(tags)))
                if not tags and not filename_bits:
                    # just :Tag name ought to also try class methods
                    tags = self.get_tags(name)
                    self.debug("Discarding empty filtered list")
            if not tags:
                continue
            if filename_bits:
                filename = '/'.join(filename_bits)
                tags = self.filter_file(tags, filename)
                self.debug("%d tags matched filename %s" % (len(tags), filename))
            if tags:
                tags = self.prioritize(tags)
                tag = tags[0]
                index = original.index(tag)
                return (tag, name, index)
        return None, None, None

    def already_editing_file(self, filename):
        if not vim.current.buffer.name:
            return False
        if not os.path.exists(vim.current.buffer.name):
            return False
        return os.path.samefile(vim.current.buffer.name, filename)

    def jump_to_tag(self, tag, name, index):
        if tag is None or name is None or index is None:
            return
        # I can't rely on just :tag because the order of tags in :[count]tag
        # doesn't match the order of tags returned by taglist() due to
        # :h tag-priority sorting!
        # Doing both now because the :tag pushes the name onto the tag stack,
        # and then my :e will make sure I went to the right location.
        self.command("%dtag %s" % (index + 1, name))
        if not self.already_editing_file(tag['filename']):
            # trying to :e the current file will fail if it's modified,
            # even if you have hidden set
            self.command("keepjumps e %s" % tag["filename"])

        tagcmd = tag["cmd"]
        if tagcmd.startswith('/^') and tagcmd.endswith('$/'):
            # tags files contain stuff like /^def foo(**kwargs):$/ which needs to be verynomagick'ed
            tagcmd = r'/^\V%s\$/' % tagcmd[2:-2].replace('\\', '\\\\')

        if tag.get('class') and tag['filename'].endswith('.py'):
            # Problem: when you've got a Python file with multiple classes
            # defining the same method (same name and signature), e.g.
            #
            # class Foo(object):
            #     def do_stuff(self):
            #         ....
            # class Bar(Foo):
            #     def do_stuff(self):
            #         ....
            #
            # you get a tags file that lists two do_stuff tags with the same
            # search pattern:
            #
            # do_stuff	foo.py	/^    def do_stuff(self):$/;"	m	class:Foo
            # do_stuff	foo.py	/^    def do_stuff(self):$/;"	m	class:Bar
            #
            # and when you :2tag clean you end up in the same place as you do
            # when you :tag clean -- on Foo.do_stuff, because it's 1st.
            #
            # So here's a workaround: first find the right class, then find
            # the right method in that class.
            self.debug("Applying Python class method workaround")
            self.command(r"keepjumps 0;/^class %s\>/;%s" % (tag['class'], tagcmd))
        else:
            self.command("keepjumps 0;%s" % tagcmd)


def jump(query):
    verbose = int(vim.eval('&verbose'))

    if not query:
        # XXX: it'd be nice to take the topmost name from the tag stack
        return

    finder = SmartTagFinder(verbose=verbose)
    tag, name, index = finder.find_best_tag(query)

    if not tag:
        print("Couldn't find %s" % query)
        return

    finder.jump_to_tag(tag, name, index)
