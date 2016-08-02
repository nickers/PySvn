import collections
import os.path
import svn.common
import svn.constants
import xml.etree.ElementTree


class LocalClient(svn.common.CommonClient):
    def __init__(self, path_, *args, **kwargs):
        if os.path.exists(path_) is False:
            raise EnvironmentError("Path does not exist: %s" % (path_))

        super(LocalClient, self).__init__(
            path_,
            svn.constants.LT_PATH,
            *args, **kwargs)

    def update(self, revision=None):
        cmd = []
        if revision is not None:
            cmd = ['-r', str(revision)]
        cmd += [self.path]

        self.run_command('update', cmd)

    def switch(self, repo_path, revision=None):
        cmd = []
        if revision is not None:
            cmd = ['-r', str(revision)]
        cmd += ['^' + repo_path, self.path]

        self.run_command('switch', cmd)

    def rm(self, path):
        return self.run_command('rm', [path])

    def status(self, path=None):
        if path is not None:
            path = os.path.join(self.path, path)
        else:
            path = self.path
        xmlRes = self.run_command('status', ['--xml', path])
        root = xml.etree.ElementTree.fromstring(xmlRes)
        se = collections.namedtuple('StatusEntry', ['path', 'status'])
        return [se(path=e.attrib['path'], status=e.find('wc-status').attrib['item']) for e in root.findall('target/entry')]


    def __repr__(self):
        return ('<SVN(LOCAL) %s>' % (self.path))
