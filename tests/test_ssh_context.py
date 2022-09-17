import os,sys
import unittest
import socket

from paramiko.ssh_exception import SSHException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
__package__ = 'tests'
from .context import SSHSession
from .context import Machine
from .sample_class import SampleClass


@unittest.skipIf(os.environ.get('DPDISPATCHER_TEST') != 'ssh', "outside the ssh testing environment")
class TestSSHContext(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mdata = {
            "batch_type": "Shell",
            "context_type": "SSHContext",
            "local_root": "./test_context_dir",
            "remote_root": "/dpdispatcher_working",
            "remote_profile": {
                "hostname": "server",
                "port": 22,
                "username": "root",
                "password": "dpdispatcher",
            },
        }
        try:
            cls.machine = Machine.load_from_dict(mdata)
        except (SSHException, socket.timeout):
            raise unittest.SkipTest("SSHException ssh cannot connect")
        cls.submission = SampleClass.get_sample_submission()
        cls.submission.bind_machine(cls.machine)
        cls.submission_hash = cls.submission.submission_hash
        file_list = ['bct-1/log.lammps', 'bct-2/log.lammps', 'bct-3/log.lammps', 'bct-4/log.lammps']
        for file in file_list:
            cls.machine.context.sftp.mkdir(os.path.join(cls.machine.context.remote_root, os.path.dirname(file)))
            cls.machine.context.write_file(file, '# mock log')

    @classmethod
    def tearDownClass(cls):
        cls.machine.context.clean()
        # close the server
        cls.machine.context.close()
    
    def setUp(self):
        self.context = self.__class__.machine.context

    def test_ssh_session(self):
        self.assertIsInstance(
            self.__class__.machine.context.ssh_session, SSHSession
        )

    def test_upload(self):
        self.context.upload(self.__class__.submission)
        check_file_list = ['graph.pb', 'bct-1/conf.lmp', 'bct-4/input.lammps']
        for file in check_file_list:
            self.assertTrue(self.context.check_file_exists(os.path.join(self.context.remote_root, file)))

    def test_download(self):
        self.context.download(self.__class__.submission)


@unittest.skipIf(os.environ.get('DPDISPATCHER_TEST') != 'ssh', "outside the ssh testing environment")
class TestSSHContextNoCompress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mdata = {
            "batch_type": "Shell",
            "context_type": "SSHContext",
            "local_root": "./test_context_dir",
            "remote_root": "/dpdispatcher_working",
            "remote_profile": {
                "hostname": "server",
                "port": 22,
                "username": "root",
                "password": "dpdispatcher",
                "tar_compress": False,
            },
        }
        try:
            cls.machine = Machine.load_from_dict(mdata)
        except (SSHException, socket.timeout):
            raise unittest.SkipTest("SSHException ssh cannot connect")
        cls.submission = SampleClass.get_sample_submission()
        cls.submission.bind_machine(cls.machine)
        cls.submission_hash = cls.submission.submission_hash
        file_list = ['bct-1/log.lammps', 'bct-2/log.lammps', 'bct-3/log.lammps', 'bct-4/log.lammps']
        for file in file_list:
            cls.machine.context.sftp.mkdir(os.path.join(cls.machine.context.remote_root, os.path.dirname(file)))
            cls.machine.context.write_file(file, '# mock log')

    @classmethod
    def tearDownClass(cls):
        cls.machine.context.clean()
        # close the server
        cls.machine.context.close()
    
    def setUp(self):
        self.context = self.__class__.machine.context

    def test_ssh_session(self):
        self.assertIsInstance(
            self.__class__.machine.context.ssh_session, SSHSession
        )

    def test_upload(self):
        self.context.upload(self.__class__.submission)
        check_file_list = ['graph.pb', 'bct-1/conf.lmp', 'bct-4/input.lammps']
        for file in check_file_list:
            self.assertTrue(self.context.check_file_exists(os.path.join(self.context.remote_root, file)))

    def test_download(self):
        self.context.download(self.__class__.submission)
        


