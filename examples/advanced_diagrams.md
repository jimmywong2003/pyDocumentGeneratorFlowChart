# Advanced Mermaid Diagrams Example

This example demonstrates various Mermaid diagram types beyond basic flowcharts.

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database

    User->>Frontend: Submit Form
    Frontend->>Backend: POST /api/data
    Backend->>Database: Query Data
    Database-->>Backend: Return Results
    Backend-->>Frontend: JSON Response
    Frontend-->>User: Display Results
```

## Class Diagram

```mermaid
classDiagram
    class User {
        +String username
        +String email
        +Date createdAt
        +login()
        +logout()
    }
    
    class Post {
        +String title
        +String content
        +User author
        +publish()
        +edit()
    }
    
    class Comment {
        +String text
        +User author
        +Post post
        +addVote()
    }
    
    User "1" -- "*" Post : creates
    User "1" -- "*" Comment : writes
    Post "1" -- "*" Comment : has
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start Request
    Processing --> Success: Operation Complete
    Processing --> Error: Operation Failed
    Success --> Idle: Reset
    Error --> Idle: Reset after Timeout
    
    state Error {
        [*] --> LogError
        LogError --> NotifyAdmin
        NotifyAdmin --> WaitRetry
        WaitRetry --> [*]
    }
```

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Development
    Design Phase      :a1, 2025-01-01, 30d
    Implementation    :after a1, 45d
    Testing           :2025-03-01, 30d
    section Deployment
    Staging           :2025-04-01, 14d
    Production        :2025-04-15, 7d
```

## Pie Chart

```mermaid
pie title Programming Language Usage
    "Python" : 45
    "JavaScript" : 30
    "Java" : 15
    "Other" : 10
```

## Testing Guidelines

### Expected Output
- Sequence Diagram: 1 PNG
- Class Diagram: 1 PNG  
- State Diagram: 1 PNG
- Gantt Chart: 1 PNG
- Pie Chart: 1 PNG
- Total: 5 PNG files

### Test Commands
```bash
# Generate complete DOCX with all diagrams
python export_document.py examples/advanced_diagrams.md

# Export only diagrams to PNG
python export_flowcharts_only.py examples/advanced_diagrams.md

# Expected output directory: flowchats/ with 5 PNG files
```

### Verification
- Check that all diagram types are properly rendered
- Verify PNG files are created with correct content
- Test both DOCX generation and PNG export functionality
