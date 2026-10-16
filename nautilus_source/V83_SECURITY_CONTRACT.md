# Nautilus Presentismo — Access and quarterly license security (V83 design contract)

## Roles
- SUPERADMIN: first-run provisioning only; sole authority to add/deactivate/reset administrators and manage licensing. Never ship a preset universal password.
- ADMIN: David Ayub, Enzo Ahumada, Alejandro Diesel, Mario De Mingo. Separate accounts, credentials individually established at activation. No credential or universal PIN committed to GitHub.
- Admin user records are not employee/personnel records. Keep these namespaces separate.

## Access enforcement
- Require authentication before all personnel, reports, imports, exports, settings and data views.
- Protect entry points, not only navigation buttons. Log out and require authentication on session expiration or app reopen.
- Store salted password hashes using a modern password KDF; never store plaintext passwords or display them in logs.
- Only the authenticated SUPERADMIN can add/disable/reset administrators. Changes are auditable.
- Initial SUPERADMIN password is chosen interactively on a trusted device on first enrollment. Recovery must not be a hardcoded bypass.

## Licenses
- Three-calendar-month activation period; display valid-until date in app.
- Graceful expired behavior: lock operational screens, preserve all SQLite staff/attendance data and allow SUPERADMIN activation and backups; never wipe records.
- Favor a backend issuing short numeric license codes, validated online, or signed offline activation tokens verifiable using a public key built into the APK.
- Never include the private signing key / generator secret in APK, repository or distributed installation ZIP.
- For device-bound licensing, capture an installation identifier and sign that with the expiry date. Prevent cross-device reuse and clock rollback where feasible. Purely offline enforcement cannot prevent tampering/repackaging by sophisticated attackers.
- Avoid silent 90-day assumptions: quarterly expiry is based on calendar date relative to last activation, with timezone-independent UTC storage.
- If users require the superadmin to issue a code *inside* the app, provision a secure signing backend with superadmin authentication, rather than embedding an extractable signing secret.

## Provisioned administrators (awaiting individual password creation)
1. David Ayub
2. Enzo Ahumada
3. Alejandro Diesel
4. Mario De Mingo

## Migration and acceptance
- Preserve existing app package ID and signing continuity for updates.
- Preserve existing people, punches and scheduled_shifts SQLite tables.
- Do not activate access lock until superadmin enrollment / valid license flow has been confirmed on a test installation; guard against trapping the owner out of live data.
- Check different administrators cannot open superadmin features, can change their own credentials, and logging out clears the session.
- Test expiry with simulated clocks; return to operation after renewal without losing records.
- Validate release APK on Android and produce one ZIP containing the installable APK after successful CI and manual checks.
