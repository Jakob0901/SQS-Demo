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

**\<Diagram or Table>**

**\<optionally: Explanation of external domain interfaces>**

## Technical Context

**\<Diagram or Table>**

**\<optionally: Explanation of technical interfaces>**

**\<Mapping Input/Output to Channels>**

# 4 Solution Strategy

| Quality Goal | Scenario | Solution Approach                                                                | Link to Details |
|--------------|-----|----------------------------------------------------------------------------------|-----------------|
| Performance  | Users expect quick response times for interactions.  | Optimize database queries, use caching mechanisms, and implement load balancing. | Section 5.1     |
| Scalability  | The application must handle an increasing number of users and quotes.  | Design for horizontal scaling, use container orchestration (e.g., Kubernetes).   | Section 5.2     |
| Security     | Protect user data and ensure secure interactions.  | Implement encryption, secure authentication, and regular security audits.        | Section 5.3     |
| Reliability     | Ensure minimal downtime and robust failover mechanisms.  | Use redundant systems, implement health checks, and monitor system performance.  | Section 5.4     |
| Usability     | Provide an intuitive and engaging user experience.  | Conduct user testing, follow UX best practices, and gather user feedback.        | Section 5.5     |
| Data Integrity     | Ensure data is stored reliably and accurately.  | Use a SQL database (PostgreSQL) to ensure data integrity and reliability.        | Section 5.6     |
| Integration     | Ensure easy integration with other services and applications.  | Design with RESTful APIs to facilitate seamless integration.        | Section 5.7     |

# 5 Building Block View 

## Whitebox Overall System 

***\<Overview Diagram>***

Motivation

:   *\<text explanation>*

Contained Building Blocks

:   *\<Description of contained building block (black boxes)>*

Important Interfaces

:   *\<Description of important interfaces>*

### \<Name black box 1> {#__name_black_box_1}

*\<Purpose/Responsibility>*

*\<Interface(s)>*

*\<(Optional) Quality/Performance Characteristics>*

*\<(Optional) Directory/File Location>*

*\<(Optional) Fulfilled Requirements>*

*\<(optional) Open Issues/Problems/Risks>*

### \<Name black box 2> {#__name_black_box_2}

*\<black box template>*

### \<Name black box n> {#__name_black_box_n}

*\<black box template>*

### \<Name interface 1> {#__name_interface_1}

...

### \<Name interface m> {#__name_interface_m}

## Level 2 {#_level_2}

### White Box *\<building block 1>* {#_white_box_emphasis_building_block_1_emphasis}

*\<white box template>*

### White Box *\<building block 2>* {#_white_box_emphasis_building_block_2_emphasis}

*\<white box template>*

...

### White Box *\<building block m>* {#_white_box_emphasis_building_block_m_emphasis}

*\<white box template>*

## Level 3 {#_level_3}

### White Box \<\_building block x.1\_\> {#_white_box_building_block_x_1}

*\<white box template>*

### White Box \<\_building block x.2\_\> {#_white_box_building_block_x_2}

*\<white box template>*

### White Box \<\_building block y.1\_\> {#_white_box_building_block_y_1}

*\<white box template>*

# 6 Runtime View {#section-runtime-view}

## \<Runtime Scenario 1> {#__runtime_scenario_1}

-   *\<insert runtime diagram or textual description of the scenario>*

-   *\<insert description of the notable aspects of the interactions
    between the building block instances depicted in this diagram.\>*

## \<Runtime Scenario 2> {#__runtime_scenario_2}

## ... {#_}

## \<Runtime Scenario n> {#__runtime_scenario_n}

# 7 Deployment View {#section-deployment-view}

## Infrastructure Level 1 {#_infrastructure_level_1}

***\<Overview Diagram>***

Motivation

:   *\<explanation in text form>*

Quality and/or Performance Features

:   *\<explanation in text form>*

Mapping of Building Blocks to Infrastructure

:   *\<description of the mapping>*

## Infrastructure Level 2 {#_infrastructure_level_2}

### *\<Infrastructure Element 1>* {#__emphasis_infrastructure_element_1_emphasis}

*\<diagram + explanation>*

### *\<Infrastructure Element 2>* {#__emphasis_infrastructure_element_2_emphasis}

*\<diagram + explanation>*

...

### *\<Infrastructure Element n>* {#__emphasis_infrastructure_element_n_emphasis}

*\<diagram + explanation>*

# 8 Cross-cutting Concepts {#section-concepts}

## *\<Concept 1>* {#__emphasis_concept_1_emphasis}

*\<explanation>*

## *\<Concept 2>* {#__emphasis_concept_2_emphasis}

*\<explanation>*

...

## *\<Concept n>* {#__emphasis_concept_n_emphasis}

*\<explanation>*

# 9 Architecture Decisions {#section-design-decisions}

Architecture decisions are recorded in the adr folder located at documentation/adr.

# 10 Quality Requirements {#section-quality-scenarios}

## Quality Tree {#_quality_tree}

## Quality Scenarios {#_quality_scenarios}

# 11 Risks and Technical Debts {#section-technical-risks}

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
