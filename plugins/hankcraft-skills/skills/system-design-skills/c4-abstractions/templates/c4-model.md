# C4 Model — <system name>

> Markdown handoff produced by the `c4-abstractions` skill. Consumed by the `likec4` skill to emit `.c4` source.
> Fill every section. The Element Registry and Relationships tables are the source of truth; ASCII diagrams must match them.

---

## System Context

<One paragraph: what is the system, who uses it, what external systems it depends on. Plain English.>

```
                    +-------------------+
                    | customer          |
                    | [person]          |
                    | Personal Banking  |
                    | Customer          |
                    +-------------------+
                              |
                              | views balance, makes payments
                              v
+= internet-banking : Internet Banking System =====================+
|                                                                  |
|                  (opened in Containers section)                  |
|                                                                  |
+==================================================================+
                              |
                              | gets account info / HTTPS+JSON
                              v
                    +-------------------+
                    | mainframe         |
                    | [existingsystem]  |
                    | Mainframe Banking |
                    +-------------------+
```

> Repeat the boundary box collapsed in this section. It is opened only in the Containers section below.

---

## Containers

<One paragraph: what the system is made of internally, the high-level shape.>

```
+= internet-banking : Internet Banking System ==========================================+
|                                                                                       |
|   +------------+     +------------+     +------------------+     +----------------+   |
|   | spa-app    |     | mobile-app |     | api-application  |     | web-application|   |
|   | [spa]      |     | [mobileApp]|     | [container]      |     | [container]    |   |
|   | JS+Angular |     | Xamarin    |     | Java + Spring    |     | Java + Spring  |   |
|   +------------+     +------------+     +------------------+     +----------------+   |
|         |                  |                     |                                    |
|         |                  |                     | reads/writes / JDBC                |
|         |                  |                     v                                    |
|         |                  |             +-------------------+                        |
|         |                  |             | db                |                        |
|         |                  |             | [database]        |                        |
|         |                  |             | Oracle 19c        |                        |
|         |                  |             +-------------------+                        |
|         |                  |                                                          |
+=======================================================================================+
        ^                  ^                       ^
        | HTTPS            | HTTPS                 | HTTPS+JSON
        |                  |                       |
   +-----------+      +-----------+         (external entry already
   | customer  |      | customer  |          shown in Context section)
   | [person]  |      | [person]  |
   +-----------+      +-----------+
```

> The system boundary is opened here. Children are containers. Off-the-shelf data stores (`database`, queue, cache) are drawn as containers but are not zoomed into in the Components section.

---

## Components — api-application

<One paragraph: what is inside this container and why we are opening it.>

```
+= api-application : API Application ==========================================+
|                                                                              |
|   +-------------------+   +---------------------+   +--------------------+   |
|   | signin-ctrl       |   | accounts-ctrl       |   | reset-pwd-ctrl     |   |
|   | [component]       |   | [component]         |   | [component]        |   |
|   | Spring MVC        |   | Spring MVC          |   | Spring MVC         |   |
|   +-------------------+   +---------------------+   +--------------------+   |
|            |                       |                         |               |
|            v                       v                         v               |
|   +-------------------+   +---------------------+   +--------------------+   |
|   | security-cmp      |   | mainframe-facade    |   | email-cmp          |   |
|   | [component]       |   | [component]         |   | [component]        |   |
|   | Spring Bean       |   | Spring Bean         |   | Spring Bean        |   |
|   +-------------------+   +---------------------+   +--------------------+   |
|                                                                              |
+==============================================================================+
            ^                       ^                         ^
            | HTTPS+JSON            | HTTPS+JSON              | HTTPS+JSON
       (from spa-app, mobile-app — see Relationships table)
```

> Repeat one `## Components — <container-id>` section per container you choose to zoom into. Skip off-the-shelf containers; record skipped ones as: `## Components — db (skipped: managed database)`.

---

## Element Registry

| id | kind | parent | label | technology | description |
| --- | --- | --- | --- | --- | --- |
| customer | person |  | Personal Banking Customer |  | Uses the bank's internet banking system. |
| mainframe | existingsystem |  | Mainframe Banking System |  | Core banking ledger; not under design. |
| internet-banking | softwaresystem |  | Internet Banking System |  | The system under design. |
| spa-app | spa | internet-banking | Single-Page Application | JavaScript + Angular | Browser UI. |
| mobile-app | mobileApp | internet-banking | Mobile App | Xamarin | Limited mobile UI. |
| web-application | container | internet-banking | Web Application | Java + Spring MVC | Serves static assets + SPA shell. |
| api-application | container | internet-banking | API Application | Java + Spring MVC | JSON/HTTPS API for the SPA and mobile app. |
| db | database | internet-banking | Database | Oracle 19c | User registration, hashed credentials, access logs. |
| signin-ctrl | component | api-application | Sign-In Controller | Spring MVC | Authenticates users. |
| accounts-ctrl | component | api-application | Accounts Summary Controller | Spring MVC | Returns account summaries. |
| reset-pwd-ctrl | component | api-application | Reset Password Controller | Spring MVC | Single-use password reset URLs. |
| security-cmp | component | api-application | Security Component | Spring Bean | Sign-in / password change logic. |
| mainframe-facade | component | api-application | Mainframe Banking System Facade | Spring Bean | Wraps mainframe calls. |
| email-cmp | component | api-application | Email Component | Spring Bean | Sends transactional email. |

---

## Relationships

| source | target | label | technology |
| --- | --- | --- | --- |
| customer | internet-banking | views account balances, makes payments |  |
| internet-banking | mainframe | gets account info, makes payments | HTTPS + JSON |
| customer | spa-app | uses | HTTPS |
| customer | mobile-app | uses | HTTPS |
| customer | web-application | visits site | HTTPS |
| web-application | spa-app | delivers to browser | HTTPS |
| spa-app | signin-ctrl | calls | HTTPS + JSON |
| spa-app | accounts-ctrl | calls | HTTPS + JSON |
| spa-app | reset-pwd-ctrl | calls | HTTPS + JSON |
| mobile-app | signin-ctrl | calls | HTTPS + JSON |
| mobile-app | accounts-ctrl | calls | HTTPS + JSON |
| mobile-app | reset-pwd-ctrl | calls | HTTPS + JSON |
| signin-ctrl | security-cmp | uses |  |
| accounts-ctrl | mainframe-facade | uses |  |
| reset-pwd-ctrl | security-cmp | uses |  |
| reset-pwd-ctrl | email-cmp | uses |  |
| security-cmp | db | reads/writes | JDBC |
| mainframe-facade | mainframe | calls | HTTPS + JSON |
