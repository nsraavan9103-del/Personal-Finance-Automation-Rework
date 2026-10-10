: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:07,872 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:07,872 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:07,872 INFO sqlalchemy.engine.Engine [cached since 4.737s ago] ()
2026-09-23 00:13:07,872 INFO sqlalchemy.engine.Engine ROLLBACK
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 4.737s ago] ()
INFO     sqlalchemy.engine.Engine:base.py:2704 ROLLBACK
________________ ERROR at setup of TestUploadAPI.test_upload_invalid_csv_fails _________________
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_api_endpoints.py:25: in clean_db
    await session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:08,228 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:08,228 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:08,228 INFO sqlalchemy.engine.Engine [cached since 5.086s ago] ()
2026-09-23 00:13:08,229 INFO sqlalchemy.engine.Engine ROLLBACK
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 5.086s ago] ()
INFO     sqlalchemy.engine.Engine:base.py:2704 ROLLBACK
_____________ ERROR at setup of TestSummaryService.test_get_expense_summary_empty ______________
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:08,866 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:08,867 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:08,867 INFO sqlalchemy.engine.Engine [cached since 5.725s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 5.725s ago] ()
________ ERROR at setup of TestSummaryService.test_get_expense_summary_single_category _________
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:09,214 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:09,214 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:09,214 INFO sqlalchemy.engine.Engine [cached since 6.072s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 6.072s ago] ()
______ ERROR at setup of TestSummaryService.test_get_expense_summary_multiple_categories _______
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:09,537 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:09,537 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:09,537 INFO sqlalchemy.engine.Engine [cached since 6.395s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 6.395s ago] ()
________ ERROR at setup of TestSummaryService.test_get_expense_summary_excludes_credits ________
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:09,888 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:09,888 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:09,888 INFO sqlalchemy.engine.Engine [cached since 6.754s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 6.754s ago] ()
_____ ERROR at setup of TestSummaryService.test_get_expense_summary_excludes_uncategorized _____
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:10,245 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:10,245 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:10,245 INFO sqlalchemy.engine.Engine [cached since 7.103s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 7.103s ago] ()
______ ERROR at setup of TestSummaryService.test_get_expense_summary_sorts_by_amount_desc ______
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:835: in _start_transaction
    await self._transaction.start()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\transaction.py:146: in start
    await self._connection.execute(query)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\asyncpg\connection.py:354: inexecute
    result = await self._protocol.query(query, timeout)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asyncpg/protocol/protocol.pyx:354: in query
    ???
asyncpg/protocol/protocol.pyx:735: in asyncpg.protocol.protocol.BaseProtocol._check_state
    ???
E   asyncpg.exceptions._base.InterfaceError: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.dialects.postgresql.asyncpg.AsyncAdapt_asyncpg_dbapi.InterfaceError: <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress

The above exception was the direct cause of the following exception:
tests\test_summary.py:24: in clean_db
    await db_session.execute(text("DELETE FROM transactions"))
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\ext\asyncio\session.py:461: in execute
    result = await greenlet_spawn(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201: in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2362: in execute
    return self._execute_internal(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py:2256: in _execute_internal
    result = conn.execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1418: in execute
    return meth(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py:515: in _execute_on_connection
    return connection._execute_clauseelement(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1640: in _execute_clauseelement
    ret = self._execute_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1846: in _execute_context
    return self._exec_single_context(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1986: in _exec_single_context
    self._handle_dbapi_exception(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:2355: in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py:1967: in _exec_single_context
    self.dialect.do_execute(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py:941: in do_execute
    cursor.execute(statement, parameters)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:572: in execute
    self._adapt_connection.await_(
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132: in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196: in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:508: in _prepare_and_execute
    await adapt_connection._start_transaction()
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:837: in _start_transaction
    self._handle_exception(error)
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\dialects\postgresql\asyncpg.py:784: in _handle_exception
    raise translated_error from error
E   sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
E   [SQL: DELETE FROM transactions]
E   (Background on this error at: https://sqlalche.me/e/20/rvf5)
------------------------------------ Captured stdout setup -------------------------------------
2026-09-23 00:13:10,581 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-09-23 00:13:10,582 INFO sqlalchemy.engine.Engine DELETE FROM transactions
2026-09-23 00:13:10,582 INFO sqlalchemy.engine.Engine [cached since 7.439s ago] ()
-------------------------------------- Captured log setup --------------------------------------
INFO     sqlalchemy.engine.Engine:base.py:2701 BEGIN (implicit)
INFO     sqlalchemy.engine.Engine:base.py:1846 DELETE FROM transactions
INFO     sqlalchemy.engine.Engine:base.py:1846 [cached since 7.439s ago] ()
======================================= warnings summary =======================================
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\pydantic\_internal\_config.py:291
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\pydantic\_internal\_config.py:291
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\pydantic\_internal\_config.py:291
..\..\..\AppData\Local\Programs\Python\Python311\Lib\site-packages\pydantic\_internal\_config.py:291
  C:\Users\Sraavan\AppData\Local\Programs\Python\Python311\Lib\site-packages\pydantic\_internal\_config.py:291: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.9/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

tests/test_api_endpoints.py: 17 warnings
  C:\Users\Sraavan\AppData\Local\Programs\Python\Python311\Lib\site-packages\httpx\_client.py:1437: DeprecationWarning: The 'app' shortcut is now deprecated. Use the explicit style 'transport=ASGITransport(app=...)' instead.
    warnings.warn(message, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=================================== short test summary info ====================================
ERROR tests/test_api_endpoints.py::TestCategoriesAPI::test_create_category - AttributeError: 'NoneType' object has no attribute 'send'
ERROR tests/test_api_endpoints.py::TestCategoriesAPI::test_create_duplicate_category - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesAPI::test_list_categories - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesAPI::test_delete_category - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesAPI::test_delete_uncategorized_protected - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesKeywordsAPI::test_list_keywords - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesKeywordsAPI::test_add_keyword - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestCategoriesKeywordsAPI::test_add_duplicate_keyword - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestTransactionsAPI::test_list_transactions_empty - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestTransactionsAPI::test_list_transactions_with_filters - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestTransactionsAPI::test_get_expense_summary - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestTransactionsAPI::test_update_transaction_category - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestUploadAPI::test_upload_csv_success - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestUploadAPI::test_upload_non_csv_fails - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_api_endpoints.py::TestUploadAPI::test_upload_invalid_csv_fails - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_empty - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_single_category - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_multiple_categories - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_excludes_credits - sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_excludes_uncategorized- sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
ERROR tests/test_summary.py::TestSummaryService::test_get_expense_summary_sorts_by_amount_desc -sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress
[SQL: DELETE FROM transactions]
(Background on this error at: https://sqlalche.me/e/20/rvf5)
========================== 22 passed, 21 warnings, 21 errors in 9.75s ==========================