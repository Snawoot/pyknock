import sys
import pytest
import os.path


TEST_PSK = 'testPSK'
proj_dir = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def server_instance():
    """Spawns server process and returns
    file-like object with process output."""
    import subprocess
    import time
    import os.path
    import tempfile

    exec_path = os.path.join(proj_dir, '..', 'pyknockd.py')
    tmpfile_kwargs = {"buffering" if sys.version_info > (3, 0) else "bufsize": 1, "mode": "w+"}
    with tempfile.TemporaryFile(**tmpfile_kwargs) as out:
        with tempfile.TemporaryFile(**tmpfile_kwargs) as err:
            sp = subprocess.Popen([exec_path,
                                   TEST_PSK,
                                   'echo open=$cmd $ip $af',
                                   'echo close=$cmd $ip $af'],
                                  stdout=out,
                                  stderr=out
                                  )
            time.sleep(1)
            yield (sp, out, err)
    sp.wait()


test_data = [
    pytest.param(None, 'open', '127.0.0.1', TEST_PSK, ['open=open 127.0.0.1 inet'], id='simple_open'),
    pytest.param(None, 'close', '127.0.0.1', TEST_PSK, ['close=close 127.0.0.1 inet'], id='simple_close'),
    pytest.param('1.2.3.4', 'open', '127.0.0.1', TEST_PSK, ['open=open 1.2.3.4 inet'], id='foreign_open'),
    pytest.param('1.2.3.4', 'close', '127.0.0.1', TEST_PSK, ['close=close 1.2.3.4 inet'], id='foreign_close'),
    pytest.param(None, 'open', '::1', TEST_PSK, ['open=open ::1 inet6'], id='simple_open_v6remote'),
    pytest.param(None, 'close', '::1', TEST_PSK, ['close=close ::1 inet6'], id='simple_close_v6remote'),
    pytest.param('1.2.3.4', 'open', '::1', TEST_PSK, ['open=open 1.2.3.4 inet'], id='foreign_open_v6remote'),
    pytest.param('1.2.3.4', 'close', '::1', TEST_PSK, ['close=close 1.2.3.4 inet'], id='foreign_close_v6remote'),
    pytest.param('fe20::150:560f:fec4:3', 'open', '::1', TEST_PSK, ['open=open fe20::150:560f:fec4:3 inet6'], id='v6foreign_open_v6remote'),
    pytest.param('fe20::150:560f:fec4:3', 'close', '::1', TEST_PSK, ['close=close fe20::150:560f:fec4:3 inet6'], id='v6foreign_close_v6remote'),
    pytest.param(None, 'open', '127.0.0.1', 'WRONGPSK', [], id='simple_open_wrongpsk'),
    pytest.param(None, 'close', '127.0.0.1', 'WRONGPSK', [], id='simple_close_wrongpsk'),
    pytest.param('1.2.3.4', 'open', '127.0.0.1', 'WRONGPSK', [], id='foreign_open_wrongpsk'),
    pytest.param('1.2.3.4', 'close', '127.0.0.1', 'WRONGPSK', [], id='foreign_close_wrongpsk'),
    pytest.param(None, 'open', '::1', 'WRONGPSK', [], id='simple_open_v6remote_wrongpsk'),
    pytest.param(None, 'close', '::1', 'WRONGPSK', [], id='simple_close_v6remote_wrongpsk'),
    pytest.param('1.2.3.4', 'open', '::1', 'WRONGPSK', [], id='foreign_open_v6remote_wrongpsk'),
    pytest.param('1.2.3.4', 'close', '::1', 'WRONGPSK', [], id='foreign_close_v6remote_wrongpsk'),
    pytest.param('fe20::150:560f:fec4:3', 'open', '::1', 'WRONGPSK', [], id='v6foreign_open_v6remote_wrongpsk'),
    pytest.param('fe20::150:560f:fec4:3', 'close', '::1', 'WRONGPSK', [], id='v6foreign_close_v6remote_wrongpsk'),
    #pytest.param('1.2.3.4', 'open', 'localhost', TEST_PSK, ['open=open 1.2.3.4 inet']*2, id='foreign_open_mixedremote'),
    #pytest.param('1.2.3.4', 'close', 'localhost', TEST_PSK, ['close=close 1.2.3.4 inet']*2, id='foreign_close_mixedremote'),
    #pytest.param('1.2.3.4', 'open', 'localhost', 'WRONGPSK', [], id='foreign_open_mixedremote_wrongpsk'),
    #pytest.param('1.2.3.4', 'close', 'localhost', 'WRONGPSK', [], id='foreign_close_mixedremote_wrongpsk'),
]


@pytest.mark.parametrize('sign_ip,cmd,remote_ip,psk,expected', test_data)
def test_simple(server_instance, sign_ip, cmd, remote_ip, psk, expected):
    import subprocess
    import time
    exec_path = os.path.join(proj_dir, '..', 'pyknock.py')

    subprocess.check_call([exec_path,
                          cmd,
                          remote_ip,
                          psk] +
                          (['-S', sign_ip] if sign_ip else []))
    time.sleep(1)

    (sp, out, err) = server_instance
    sp.kill()

    err.flush()
    err.seek(0)
    assert len(err.read()) == 0, "Unexpected server output"

    out.flush()
    out.seek(0)
    lines = list(map(str.rstrip, out.readlines()))
    assert lines == expected, "Unexpected server output"
