# Moviequotes

**About arc42**

arc42, the template for documentation of software and system
architecture.

Template Version 8.2 EN. (based upon AsciiDoc version), January 2023

Created, maintained and © by Dr. Peter Hruschka, Dr. Gernot Starke and
contributors. See <https://arc42.org>.

# 1 Introduction and Goals 

The primary goal of the MovieQuotes API is to provide a simple and user-friendly interface for fetching and saving movie quotes. 
The API is designed to be intuitive and easy to use and includes a Web application for easy access.

## Requirements Overview

This section describes the relevant requirements and the driving forces that software architects and development team must consider. 
These include:

- Functional Requirements: The API must allow users to fetch random quotes, search for quotes by author or movie, and save new quotes.
- Functional Requirements: The API must allow users to fetch random quotes, and save new quotes.
- Functional Requirements: The API must allow users to access a Web application that provides a user-friendly interface for interacting with the API.
- Functional Requirements: The Web application must allow users to view and save quotes.
- Non-Functional Requirements: The API must be able to handle a growing number of users and quotes without significant performance degradation.
- Non-Functional Requirements: The application must be reliable and robust, with minimal downtime and errors.
- Non-Functional Requirements: The application must be secure, with appropriate measures to protect against unauthorized access and data breaches.
- Non-Functional Requirements: The application must be intuitive and easy to use, with a clean and user-friendly interface.
- Non-Functional Requirements: The API must be performant, scalable, and secure. It should also provide a user-friendly interface for the Web application.

## Quality Goals

The architecture of the application must meet the following quality goals:

- Performance: The application should respond quickly to user interactions, ensuring a smooth and responsive experience.
- Reliability: The application should be robust and reliable, with minimal downtime and errors.
- Security: User data and interactions should be secure, with appropriate measures to protect against unauthorized access and data breaches.
- Usability: The application should be intuitive and easy to use, with a clean and user-friendly interface.
- Maintainability: The codebase should be well-structured and easy to maintain, with clear documentation and a modular design.

## Stakeholders

| Role/Name | Contact                               | Expectations                                                                                                         |
|-----------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Third-Party Service Providers | https://api.quotable.io/              | Clear integration guidelines, reliable performance, and timely support for API-related issues.                       |
| Developer | https://github.com/Jakob0901          | Well-documented and modular architecture, easy development and maintenance, access to necessary tools and resources. |
| End User | https://github.com/Jakob0901/SQS-Demo | Seamless and enjoyable user experience, intuitive interface, quick response times, and engaging features.            |
| Administrator | https://github.com/Jakob0901/SQS-Demo | Robust administrative tools, comprehensive user management, system monitoring, and security measures.                |


# 2 Architecture Constraints 

- The application must be containerized using Docker to ensure consistency across different environments and facilitate easy deployment.
- The application must be store data in a SQL database to ensure data integrity and reliability.
- The application must be built with a programming language supporting various testing frameworks like Python, Java, or C#.
- The application must be designed with restful APIs to ensure easy integration with other services and applications.

# 3 Context and Scope

## Business Context 

### Context Diagram

![Business Context Diagram](images/buisness_context_diagram.png)

### Communication Partners
| Communication Partner | Inputs                                          | Outputs                                          |
 |-----------------------|-------------------------------------------------|--------------------------------------------------|
 | Users                 | User requests, search queries, user preferences | Movie quotes, search results, user notifications |
 | External API          | API requests, authentication tokens             | Movie data, API responses                        |
 | Database              | Data queries, data updates                      | Query results, data confirmations                |
 | Build System          | Build requests, code changes                    | Build artifacts, deployment notifications        |


### Description

- **Users**: Interact with the application to search for, discover, and share movie quotes. Users provide input through the user interface and receive outputs such as search results and notifications.
- **External API**: Provides additional movie data and functionalities. The application sends API requests and receives responses containing movie data.
- **Database**: Stores and retrieves application data. The application sends data queries and updates, receiving query results and confirmations.

## Technical Context

![Technical Context Diagram](images/technical_context_diagram.png)

### Communication Partners
| Domain-Specific I/O | Channel/Protocol | Transmission Media | Description                                                                |
 |---------------------|------------------|--------------------|----------------------------------------------------------------------------|
 | User Requests       | HTTP/HTTPS       | Web browsers       | Users interact with the application through web browsers using HTTP/HTTPS. |
 | API Requests        | RESTful API      | API servers        | The application sends API requests to external APIs using RESTful API.     |
 | Data Queries        | SQL              | Database servers   | The application sends data queries to the database using SQL.              |
 | Build Requests      | CI/CD Pipeline   | Build servers      | The application sends build requests to the CI/CD pipeline for deployment. |

### Description

- **Users**: Interact with the application through web browsers and mobile devices using HTTP/HTTPS and WebSocket protocols.
- **External API**: Communicates with the application using RESTful API and HTTPS protocols. The API is hosted on API servers and cloud services.
- **Database**: Stores and retrieves application data using SQL and JDBC protocols. The database is hosted on database servers and cloud databases.
- **Build System**: The application is built and deployed using a CI/CD pipeline, which communicates with build servers and cloud services using various protocols.

# 4 Solution Strategy

| Quality Goal   | Scenario                                                              | Solution Approach                                                                | Link to Details |
|----------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------|-----------------|
| Performance    | Users expect quick response times for interactions.                   | Optimize database queries, use caching mechanisms, and implement load balancing. | Section 5.1     |
| Scalability    | The application must handle an increasing number of users and quotes. | Design for horizontal scaling, use container orchestration (e.g., Kubernetes).   | Section 5.2     |
| Security       | Protect user data and ensure secure interactions.                     | Implement encryption, secure authentication, and regular security audits.        | Section 5.3     |
| Reliability    | Ensure minimal downtime and robust failover mechanisms.               | Use redundant systems, implement health checks, and monitor system performance.  | Section 5.4     |
| Usability      | Provide an intuitive and engaging user experience.                    | Conduct user testing, follow UX best practices, and gather user feedback.        | Section 5.5     |
| Data Integrity | Ensure data is stored reliably and accurately.                        | Use a SQL database (PostgreSQL) to ensure data integrity and reliability.        | Section 5.6     |
| Integration    | Ensure easy integration with other services and applications.         | Design with RESTful APIs to facilitate seamless integration.                     | Section 5.7     |

# 5 Building Block View 

## Whitebox Overall System 

![Overall System Architecture](images/architecture-overall-whitebox.png)

Rational:
The overall system architecture is designed to provide a clear separation of concerns, with distinct layers for the Web application, API, and database.
The application is designed to connect the different components of the system.
The Web application provides a way for user interaction.
The external API provides a way to fetch random quotes.
The database provides a way to persistently store data.

## Level 2 

![Overall System Architecture](images/architecture-l2.png)

Contained Blackboxes

| Blackbox | Description                                                                                                           |
|----------|-----------------------------------------------------------------------------------------------------------------------|
| app      | Handles HTTP requests and responses, providing a user-friendly interface for interacting with the API.                |
| index    | Provides the main page for the Web application, allowing users to view and save quotes.                               |
| wrapper  | Provides a consistent interface for interacting with external services, such as the third-party API for movie quotes. |
| database | Handles the interaction with the SQL database, including saving and retrieving quotes.                                |

### Blackbox 

#### app

The app is the main entry point for the application, handling HTTP requests and responses.
It uses Flask to create a web application that provides a user-friendly interface for interacting with the API.
It includes routes for fetching random quotes, saving quotes, and retrieving stored quotes.
The functionality of the app is divided into several routes, each responsible for a specific action.
The app also includes error handling and logging to ensure a smooth user experience.

#### index

Contains the main page for the Web application, allowing users to view and save quotes.
It provides a user-friendly interface for interacting with the API and includes features such as, viewing random quotes, and saving and retrieving favorite quotes.

#### wrapper

The wrapper python package contains all wrapper classes for the application.
Thereby a wrapper is split into two parts:
- Internal wrapper: This is the main wrapper class that provides a consistent interface for interacting with external services, such as the third-party API for movie quotes.
- External wrapper: This is the wrapper class that provides a consistent interface for interacting with the external API, allowing the application to fetch random quotes and save quotes.

External wrapper are stored in the subpackages.
Those can contain multiplw wrapper classes implementing different external APIs to solve the same issue.

#### database

The database python package contains all database-related classes and functions for the application.
The main class is Storage that contains the implementation of the connection with the postgresql database.

# 6 Runtime View {#section-runtime-view}

## Request Quote

![Runtime View - Request Quote](images/runtime-request-quote.png)

1. Try get_quote: access on the api to retrieve a random quote.
2. Request get_random_quote: Call the wrapper class to get a random quote from the third-party API.
3. get_quote_random: call the http client to get a random quote from the third-party API.
4. request.get: Send a GET request to the third-party API to retrieve a random quote.

## Save Quote

![Runtime View - Save Quote](images/runtime-save-quote.png)

1. Try save_quote: access on the api to save a quote.
2. require_api_key: Check if the API key is valid.
3. store_quote: Call the wrapper class to save the quote in the database.
4. SQL-Request: Use SQLAlchemy to interact with the database and save the quote.

## Retrieve saved Quotes

# 7 Deployment View 

![Deployment View Overview](images/deployment-view-overview.png)

1. Try get_stored_quotes: access on the api to retrieve stored quotes.
2. require_api_key: Check if the API key is valid.
3. get_stored_quotes: Call the wrapper class to retrieve stored quotes from the database.
4. SQL-Request: Use SQLAlchemy to interact with the database and retrieve stored quotes.

**Content**

The deployment view describes:

- The technical infrastructure used to execute your system, including environments, servers, processors, channels, network topologies, and other infrastructure elements.
- The mapping of (software) building blocks to these infrastructure elements.

**Motivation**

Software does not run without hardware. 
This underlying infrastructure can and will influence your system and/or some cross-cutting concepts. 
Therefore, you need to know the infrastructure.

## Infrastructure Level 1 

Description

The movie quotes application is deployed across multiple environments to ensure development, testing, and production needs are met. 
The infrastructure includes:

**_Overview Diagram_**

![Level 1 Overview](images/architecture-l1.png)

Motivation

:   The deployment structure is designed to ensure high availability, low latency, and efficient resource utilization. 
The application is deployed in a cloud environment, ensuring scalability and flexibility.
The application is containerized using Docker, allowing for easy deployment and management of services.
By utilizing a microservices architecture, the application can be easily maintained.

Quality and/or Performance Features

:   **High Availability**:The application is designed to be highly available by utilizing a microservices architecture, that can be quickly booted, modified and scaled as needed.<br>
**Scalability**: The cloud-based infrastructure allows for easy scaling of resources to handle increased load and user base.<br>
**Security**: The application is designed with security in mind, utilizing encryption and secure authentication methods to protect user data and interactions.

Mapping of Building Blocks to Infrastructure

:  **Production Enviroment:** The production environment is where the application is deployed and accessed by end-users.
**Cloud VMs**: The application is deployed on cloud-based virtual machines (VMs) to ensure scalability and flexibility.
**Cloud Infrastructure**: The application is hosted on a cloud infrastructure, allowing for easy scaling and management of resources.

## Infrastructure Level 2 {#_infrastructure_level_2}

### Application 

**Overview Diagram**

![Level 2 Overview](images/architecture-l2.png)

**Explanation**
:   **Restful APIs**: The application is designed with RESTful APIs to facilitate seamless integration with other services and applications. 
It also provides a user-friendly interface for the Web application.<br>
**Database**: The application uses a SQL database (PostgreSQL) to ensure data integrity and reliability.'
**API**: The application relies on third-party services for social sharing and other functionalities.
**Web Application**: The application provides a user-friendly interface for interacting with the API, allowing users to view and save quotes.

# 8 Cross-cutting Concepts {#section-concepts}

## Authentication

**Purpose**
Prevent unauthorized access to the application and its data by implementing secure authentication mechanisms.

**Implementation**

```python
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Forbidden"}), 403

    return decorated_function
```

The implementation of authentication in the application is done using API keys.
It is implemented with a decorator function that checks the API key in the request headers.
If the API key is valid, the request is processed; otherwise, a 403 Forbidden response is returned.

**Impact**

The implementation of authentication in the application ensures that only authorized users can access the API and its resources.

## Tenacity

**Purpose**

The purpose of implementing tenacity in the application is to ensure that the application can handle transient errors and retries requests when necessary.
Transient errors can occur due to network issues, temporary unavailability of services, or other factors that may cause a request to fail.
By implementing tenacity, the application can automatically retry failed requests, improving reliability and user experience.
This is used for the connection with the the third-party API.

**Implementation**

```python
from tenacity import retry

@retry
def get_random_quote(self):
    # do request
    pass
```

The implementation of tenacity in the application is done using the tenacity library.
The `@retry` decorator is used to automatically retry the `get_random_quote` method when it fails.
This is handled in the wrapper class of the API.

**Impact**

The implementation of tenacity in the application ensures that the application can handle transient errors and retries requests when necessary.

## Logging

**Purpose**

The purpose of logging in the application is to provide a mechanism for tracking and recording events, errors, and other important information during the application's execution.
Logging is essential for debugging, monitoring, and maintaining the application, as it allows developers and administrators to understand the application's behavior and identify issues.

**Implementation**

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

logger.info("This is an info message")
```

The implementation of logging in the application is done using the built-in logging module in Python.

**Impact**

The implementation of logging in the application ensures that important events and errors are recorded, allowing developers and administrators to monitor the application's behavior and troubleshoot issues effectively.

# 9 Architecture Decisions {#section-design-decisions}

Architecture decisions are recorded in the adr folder located at documentation/adr.

# 10 Quality Requirements {#section-quality-scenarios}

## Quality Requirements Overview

| ID      | Description                                                                                                                                      |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 10.1.1  | Users can easily navigate the application and discover movie quotes without requiring extensive training or documentation.                       |
| 10.1.2  | The application provides clear and concise error messages that help users understand and resolve issues quickly.                                 |
| 10.1.3  | The application's modular architecture allows for easy updates and maintenance, with well-documented code and clear separation of concerns.      |
| 10.1.4  | Comprehensive test coverage ensures that changes to the codebase do not introduce new issues, facilitating safe and reliable updates.            |
| 10.1.5  | The application implements robust error handling and data validation to ensure reliable operation and data integrity.                            |
| 10.1.6  | The application is designed to handle high user loads efficiently, ensuring optimal performance and responsiveness even during peak usage times. |

## Quality Scenarios 

|ID|Context/Background|Sources/Stimulus| Metric/Acceptance Criteria                                                                                                                 |
|-|-|-|--------------------------------------------------------------------------------------------------------------------------------------------|
|10.2.1|Users navigating the application to discover movie quotes.|User interacts with the application interface.| Users can find and share movie quotes within 3 clicks or less, with a response time of under 2 seconds for each interaction.               |
|10.2.2|Users encountering errors while using the application.|User performs an action that results in an error.| The application displays clear and concise error messages, guiding users to resolve the issue within 10 seconds.                           |
|10.2.2|Users encountering errors while using the application.|User performs an action that results in an error.| The application displays clear and concise error messages, guiding users to resolve the issue within 10 seconds.                           |
|10.2.3|Application handling high user loads during peak usage times.|Multiple users accessing the application simultaneously.| The application maintains a response time of under 2 seconds for 95% of user interactions, even with 1000 concurrent users.                |
|10.2.4|Application performing data validation and error handling.|User submits data to the application.| The application validates data and handles errors gracefully, ensuring data integrity and providing feedback to the user within 1 second.  |


# 11 Risks and Technical Debts 

|Risk | Description                                                                                                                                                                                               |
|-|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Integration with Third-Party Services| The application relies on third-party services for social sharing and other functionalities. Any changes or disruptions in these services could impact the application's performance and user experience. |
|Data Security and Privacy| Ensuring the security and privacy of user data is critical. Any breaches or non-compliance with data protection regulations could result in legal issues and loss of user trust.                          |
|Scalability and Performance| As the user base grows, the application must handle increased load without performance degradation. Inadequate scalability measures could lead to slow response times and poor user experience.           |
|Dependency on External APIs| The application depends on external APIs for various functionalities. Any changes or downtime in these APIs could affect the application's performance and reliability.                                   |
|Compatibility with Multiple Platforms| Ensuring the application is compatible with multiple platforms and devices is challenging. Inadequate testing and optimization could result in a poor user experience on certain platforms.               |
|Compliance with Legal and Regulatory Requirements| The application must comply with various legal and regulatory requirements. Non-compliance could result in legal issues, fines, and damage to the application's reputation.                               |
|Maintenance and Support| Providing ongoing maintenance and support is essential for the application's success. Inadequate resources or planning could lead to unresolved issues and reduced user satisfaction.                     |

# 12 Glossary {#section-glossary}

+-----------------------+-----------------------------------------------+
| Term                  | Definition                                    |
+=======================+===============================================+
| *\<Term-1>*           | *\<definition-1>*                             |
+-----------------------+-----------------------------------------------+
| *\<Term-2>*           | *\<definition-2>*                             |
+-----------------------+-----------------------------------------------+
