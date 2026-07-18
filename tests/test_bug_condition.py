# tests/test_bug_condition.py
#
# Bug Condition Exploration Test
# Property 1: Plugin Fails to Import on Python 3.11+
#
# **Validates: Requirements 1.1, 1.2, 1.4, 1.5**
#
# This test encodes the EXPECTED behavior after migration:
#   - python-telegram-bot v20+ Application API is importable and usable
#   - The v13 patterns (Filters class, Request module, Updater v13 API) are gone
#   - telegramer/core.py source code uses v20+ patterns
#
# When run on UNFIXED code with PTB v20+ installed, these tests WILL FAIL
# because core.py still uses v13 API patterns that are incompatible with v20+.
# This failure CONFIRMS the bug exists.
#
# After the fix is applied, these tests WILL PASS, confirming the bug is resolved.

import sys
import os
import pytest


# Helper: path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestBugConditionV20APIAvailable:
    """Test that python-telegram-bot v20+ API classes are importable and functional.

    These tests verify that the modern API is available. They PASS on both
    unfixed and fixed code because they test the library, not the plugin.
    They establish that the v20+ API is the correct target.
    """

    def test_application_class_available(self):
        """Application class (v20+ replacement for Updater-based bot setup) is available."""
        from telegram.ext import Application, ApplicationBuilder
        assert Application is not None
        assert ApplicationBuilder is not None

    def test_filters_module_available(self):
        """filters module (lowercase, v20+) provides TEXT, Document, Regex."""
        from telegram.ext import filters
        assert hasattr(filters, "TEXT")
        assert hasattr(filters, "Document")
        assert hasattr(filters, "Regex")

    def test_context_types_available(self):
        """ContextTypes is available for type hints in v20+."""
        from telegram.ext import ContextTypes
        assert ContextTypes.DEFAULT_TYPE is not None


class TestBugConditionV13PatternsIncompatible:
    """Test that v13 API patterns used by core.py are incompatible with PTB v20+.

    These tests prove that the specific patterns used in the unfixed core.py
    CANNOT work with python-telegram-bot v20+. Each test corresponds to a
    specific line/pattern in core.py that will break.
    """

    def test_filters_class_not_available(self):
        """Filters (capital F) class used by core.py is removed in v20+.

        core.py uses: from telegram.ext import (..., Filters)
        And then: Filters.text, Filters.document, Filters.regex(r'magnet:?')
        """
        with pytest.raises(ImportError):
            from telegram.ext import Filters  # noqa: F401

    def test_telegram_utils_request_not_available(self):
        """telegram.utils.request.Request used by core.py is removed in v20+.

        core.py uses: from telegram.utils.request import Request
        And then: bot_request = Request(**REQUEST_KWARGS)
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from telegram.utils.request import Request  # noqa: F401

    def test_updater_v13_init_pattern_fails(self):
        """Updater(bot=bot, use_context=True, request_kwargs=...) pattern fails in v20+.

        core.py uses: self.updater = Updater(bot=self.bot, use_context=True, request_kwargs=REQUEST_KWARGS)
        In v20+, Updater.__init__ only accepts (bot, update_queue) - no use_context, no request_kwargs.
        """
        from telegram.ext import Updater

        with pytest.raises(TypeError):
            # This is the exact pattern from core.py enable() method
            Updater(bot=None, use_context=True, request_kwargs={})

    def test_updater_has_no_dispatcher(self):
        """Updater.dispatcher attribute used by core.py doesn't exist in v20+.

        core.py uses: dp = self.updater.dispatcher
        In v20+, Updater has no 'dispatcher' - handlers go on Application.
        """
        from telegram.ext import Updater
        assert not hasattr(Updater, 'dispatcher'), \
            "Updater should not have 'dispatcher' in v20+ (replaced by Application)"


class TestBugConditionCoreSourceUsesV13:
    """Test that telegramer/core.py source code uses v13 patterns (UNFIXED state).

    These tests read the source of core.py and verify it contains the v13
    patterns that are incompatible with PTB v20+.

    On UNFIXED code: These tests FAIL (they assert v13 patterns are ABSENT,
    but they are present) → confirms bug exists.

    On FIXED code: These tests PASS (v13 patterns replaced with v20+ equivalents).
    """

    @pytest.fixture
    def core_source(self):
        """Read core.py source code."""
        core_path = os.path.join(PROJECT_ROOT, 'telegramer', 'core.py')
        with open(core_path, 'r') as f:
            return f.read()

    def test_core_does_not_import_updater(self, core_source):
        """core.py should not import Updater (v13 class with incompatible API in v20+).

        The unfixed code has:
            from telegram.ext import (Updater, CallbackContext, CommandHandler,
                                      MessageHandler, ConversationHandler, Filters)
        """
        # Check that the import line doesn't contain Updater
        assert "Updater" not in core_source, \
            ("core.py still imports/uses Updater which has an incompatible API in v20+. "
             "Should use Application/ApplicationBuilder instead.")

    def test_core_does_not_import_filters_class(self, core_source):
        """core.py should not import Filters (capital F, removed in v20+).

        The unfixed code imports Filters and uses Filters.text, Filters.document, etc.
        """
        assert "Filters" not in core_source, \
            ("core.py still imports/uses Filters (capital F) which was removed in v20+. "
             "Should use filters.TEXT, filters.Document.ALL, filters.Regex() instead.")

    def test_core_does_not_import_request(self, core_source):
        """core.py should not import telegram.utils.request.Request (removed in v20+).

        The unfixed code has:
            from telegram.utils.request import Request
        """
        assert "telegram.utils.request" not in core_source, \
            ("core.py still imports telegram.utils.request.Request which was removed in v20+. "
             "Should use httpx-based request handling via ApplicationBuilder.")

    def test_core_does_not_use_dispatcher_pattern(self, core_source):
        """core.py should not use updater.dispatcher pattern (removed in v20+).

        The unfixed code has:
            dp = self.updater.dispatcher
            dp.add_handler(...)
        """
        assert ".dispatcher" not in core_source, \
            ("core.py still uses .dispatcher pattern which was removed in v20+. "
             "Should register handlers on Application directly.")

    def test_core_uses_application_pattern(self, core_source):
        """core.py should use Application/ApplicationBuilder (v20+ pattern).

        After fix, core.py should contain ApplicationBuilder or Application usage.
        """
        has_application = ("Application" in core_source or
                           "ApplicationBuilder" in core_source)
        assert has_application, \
            ("core.py does not use Application/ApplicationBuilder from v20+. "
             "The plugin must be migrated to the v20+ async Application API.")
