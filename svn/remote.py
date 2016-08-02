import svn.constants
import svn.common


class RemoteClient(svn.common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        super(RemoteClient, self).__init__(
            url, 
            svn.constants.LT_URL, 
            *args, **kwargs)

    def checkout(self, path, revision=None, subdir=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        url = self.url
        if subdir is not None:
            url += u'/' if url[-1] != '/' else ''
            url += subdir if subdir[:1] != '/' else subdir[1:]
        cmd += [url, path]

        self.run_command('checkout', cmd, return_binary=True)

    def mkdir(self, path, message=None, parents=False):
        cmd = []
        if parents:
            cmd += ['--parents']
        cmd += [self.url + '/' + path]
        cmd += ['-m', message if message is not None else 'created directory']
        try:
            self.run_command('mkdir', cmd)
            return True
        except ValueError as e:
            return False

    def __repr__(self):
        return ('<SVN(REMOTE) %s>' % (self.url))
