import dataclasses
import unittest

from app.server.server_options import ServerOptions, server_options_from_env, SSL_CONTEXT


class ServerOptionsFromEnvTest(unittest.TestCase):

    def test_defaults_match_the_historical_direct_tls_setup(self):
        options = server_options_from_env({})
        self.assertEqual(options, ServerOptions(host='0.0.0.0', port=5000, ssl_context=None, debug=False))

    def test_host_override(self):
        self.assertEqual(server_options_from_env({'PYTHON_HOST': '127.0.0.1'}).host, '127.0.0.1')

    def test_port_override(self):
        self.assertEqual(server_options_from_env({'PYTHON_PORT': '5001'}).port, 5001)

    def test_port_with_surrounding_whitespace_is_accepted(self):
        self.assertEqual(server_options_from_env({'PYTHON_PORT': ' 5001 '}).port, 5001)

    def test_empty_values_fall_back_to_defaults(self):
        options = server_options_from_env({'PYTHON_HOST': '', 'PYTHON_PORT': '', 'PYTHON_SSL_ON': '', 'PYTHON_DEBUG_ON': ''})
        self.assertEqual(options, server_options_from_env({}))

    def test_non_numeric_port_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'PYTHON_PORT'):
            server_options_from_env({'PYTHON_PORT': 'abc'})

    def test_port_zero_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'PYTHON_PORT'):
            server_options_from_env({'PYTHON_PORT': '0'})

    def test_port_above_range_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'PYTHON_PORT'):
            server_options_from_env({'PYTHON_PORT': '65536'})

    def test_port_at_upper_boundary_is_accepted(self):
        self.assertEqual(server_options_from_env({'PYTHON_PORT': '65535'}).port, 65535)

    def test_ssl_on_with_true_or_yes_in_any_case(self):
        for value in ['true', 'TRUE', 'yes', 'Yes']:
            with self.subTest(value=value):
                self.assertEqual(server_options_from_env({'PYTHON_SSL_ON': value}).ssl_context, SSL_CONTEXT)

    def test_ssl_off_for_false_or_unrecognised_values(self):
        for value in ['false', 'no', '1', 'garbage']:
            with self.subTest(value=value):
                self.assertIsNone(server_options_from_env({'PYTHON_SSL_ON': value}).ssl_context)

    def test_ssl_context_is_the_deployed_cert_and_key(self):
        self.assertEqual(SSL_CONTEXT, ('cert.crt', 'key.key'))

    def test_debug_on_with_true_or_yes(self):
        for value in ['true', 'YES']:
            with self.subTest(value=value):
                self.assertTrue(server_options_from_env({'PYTHON_DEBUG_ON': value}).debug)

    def test_debug_off_for_unrecognised_values(self):
        self.assertFalse(server_options_from_env({'PYTHON_DEBUG_ON': 'nope'}).debug)

    def test_debug_and_ssl_can_combine(self):
        options = server_options_from_env({'PYTHON_DEBUG_ON': 'true', 'PYTHON_SSL_ON': 'true'})
        self.assertTrue(options.debug)
        self.assertEqual(options.ssl_context, SSL_CONTEXT)

    def test_options_are_immutable(self):
        options = server_options_from_env({})
        with self.assertRaises(dataclasses.FrozenInstanceError):
            options.port = 1


if __name__ == '__main__':
    unittest.main()
