# Basic Flowchart Example

This example demonstrates a simple flowchart using Mermaid syntax.

## Simple Process Flow

```mermaid
flowchart TD
    A[Start] --> B{Input Validation}
    B -->|Valid| C[Process Data]
    B -->|Invalid| D[Show Error]
    C --> E[Generate Output]
    D --> F[End with Error]
    E --> G[End Successfully]
```

## User Registration Process

```mermaid
flowchart LR
    Start[Visit Site] --> Register[Registration Form]
    Register --> Validate[Validate Input]
    Validate -->|Valid| Create[Create Account]
    Validate -->|Invalid| Error[Show Errors]
    Create --> Confirm[Send Confirmation]
    Confirm --> Success[Registration Complete]
    Error --> Register
```

## System Architecture

```mermaid
flowchart TB
    Client[Web Browser] --> API[Backend API]
    API --> Auth[Authentication Service]
    API --> DB[(Database)]
    API --> Cache[Redis Cache]
    
    subgraph Microservices
        Auth
        UserService[User Service]
        PaymentService[Payment Service]
    end
    
    API --> UserService
    API --> PaymentService
```

## Testing Notes
- This file contains 3 different flowchart examples
- Each demonstrates different Mermaid features:
  - Basic nodes and arrows
  - Conditional logic (diamond shapes)
  - Subgraphs for grouping
  - Different arrow styles

To test:
1. Use `python export_document.py examples/basic_flowchart.md` to generate DOCX
2. Use `python export_flowcharts_only.py examples/basic_flowchart.md` to export PNGs
3. Expected output: 3 PNG files in the flowchats/ directory
