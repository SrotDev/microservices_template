# Complete Booking Journey - Simplified Visualizations

## Option 1: Simple 6-Step Process

```mermaid
graph LR
    A[1. Login] --> B[2. Search Trains]
    B --> C[3. Select Seat<br/>🔒 Lock]
    C --> D[4. Verify OTP]
    D --> E[5. Pay]
    E --> F[6. Confirm<br/>🔓 Unlock]
    
    style C fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style F fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

## Option 2: Journey with Services

```mermaid
graph TD
    U[👤 User] --> |Login| AUTH[Auth Service]
    AUTH --> |JWT| U
    
    U --> |Search| TRAIN[Train Service]
    TRAIN --> |Train List| U
    
    U --> |Select Seat| BOOK[Booking Service]
    BOOK --> |Lock| REDIS[(Redis)]
    BOOK --> |Booking ID| U
    
    U --> |OTP| BOOK
    BOOK --> |Verified| U
    
    U --> |Payment| PAY[Payment Service]
    PAY --> |Success| U
    
    U --> |Confirm| BOOK
    BOOK --> |Release Lock| REDIS
    BOOK --> |Event| MQ[RabbitMQ]
    MQ --> |Notify| NOTIF[Notification]
    BOOK --> |Ticket| U
    
    style BOOK fill:#ffebee,stroke:#c62828,stroke-width:3px
    style REDIS fill:#fff9c4,stroke:#f57c00,stroke-width:2px
```

## Option 3: Horizontal Timeline

```mermaid
timeline
    title Train Ticket Booking Journey
    
    section Authentication
        Login : User enters credentials
              : System validates
              : JWT token issued
    
    section Discovery
        Search : User searches trains
               : System checks cache
               : Returns available trains
        
        Browse : User views seat layout
               : Real-time availability shown
    
    section Booking (Critical)
        Select : User clicks seat
               : Redis lock acquired (5 min)
               : Booking record created
        
        Verify : User enters OTP
               : OTP validated
               : Booking status updated
    
    section Payment
        Pay : User enters payment info
            : Payment processed (mock)
            : Payment record saved
    
    section Confirmation
        Confirm : Booking confirmed
                : Seat status updated
                : Redis lock released
                : Ticket generated
                : Email sent (async)
```

## Option 4: User Journey Map

```mermaid
journey
    title User's Train Booking Experience
    section Login
        Open website: 5: User
        Enter credentials: 4: User
        Receive JWT: 5: User
    section Search
        Search trains: 5: User
        View results: 5: User
        Select train: 5: User
    section Book Seat
        Click seat: 5: User
        Seat locked: 3: User, System
        Timer starts: 3: User
    section Verify
        Enter OTP: 4: User
        OTP verified: 5: User
    section Pay
        Enter payment: 4: User
        Payment success: 5: User
    section Complete
        Booking confirmed: 5: User, System
        Receive ticket: 5: User
        Get email: 5: User
```

## Option 5: Simplified Architecture Flow

```mermaid
flowchart LR
    USER([User]) --> FE[Frontend]
    FE --> GW[API Gateway]
    
    GW --> AUTH[Auth<br/>Service]
    GW --> TRAIN[Train<br/>Service]
    GW --> BOOK[Booking<br/>Service]
    GW --> PAY[Payment<br/>Service]
    
    BOOK <--> REDIS[(Redis<br/>Locks)]
    BOOK --> MQ[Message<br/>Queue]
    MQ --> NOTIF[Notification<br/>Service]
    
    AUTH --> DB[(Database)]
    TRAIN --> DB
    BOOK --> DB
    PAY --> DB
    
    style BOOK fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style REDIS fill:#fff9c4,stroke:#f57c00,stroke-width:3px
    style MQ fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px
```

## Option 6: Step-by-Step with Icons

```mermaid
graph TD
    S1[🌐 User Opens Website] --> S2[🔐 Login with Credentials]
    S2 --> S3[🔍 Search Trains<br/>Dhaka → Chittagong]
    S3 --> S4[🚂 Select Train]
    S4 --> S5[💺 Choose Seat]
    
    S5 --> LOCK{🔒 Is Seat<br/>Available?}
    LOCK -->|❌ No| S5
    LOCK -->|✅ Yes| S6[⏱️ Seat Locked<br/>5 Minutes]
    
    S6 --> S7[📱 Enter OTP]
    S7 --> S8[💳 Enter Payment]
    S8 --> S9[✅ Confirm Booking]
    S9 --> S10[🔓 Release Lock]
    S10 --> S11[🎫 Generate Ticket]
    S11 --> S12[📧 Send Email]
    S12 --> END[🎉 Done!]
    
    S6 -.->|⏰ Timeout| EXPIRE[❌ Lock Expired]
    EXPIRE -.-> S5
    
    style LOCK fill:#fff9c4,stroke:#f57c00,stroke-width:3px
    style S6 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style S10 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style END fill:#81c784,stroke:#1b5e20,stroke-width:3px
```

## Option 7: Data Flow Diagram

```mermaid
graph TB
    subgraph Input
        I1[User Credentials]
        I2[Search Query]
        I3[Seat Selection]
        I4[OTP Code]
        I5[Payment Info]
    end
    
    subgraph Processing
        P1[Authentication]
        P2[Train Query]
        P3[Seat Locking]
        P4[OTP Verification]
        P5[Payment Processing]
        P6[Booking Confirmation]
    end
    
    subgraph Output
        O1[JWT Token]
        O2[Train List]
        O3[Booking ID]
        O4[Verification Status]
        O5[Payment Receipt]
        O6[Ticket]
    end
    
    I1 --> P1 --> O1
    I2 --> P2 --> O2
    I3 --> P3 --> O3
    I4 --> P4 --> O4
    I5 --> P5 --> O5
    O1 & O2 & O3 & O4 & O5 --> P6 --> O6
    
    style P3 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style P6 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

## Option 8: Minimal Clean Flow

```mermaid
flowchart TD
    START([Start]) --> LOGIN[Login]
    LOGIN --> SEARCH[Search Trains]
    SEARCH --> SELECT[Select Seat]
    
    SELECT --> LOCK{Lock<br/>Acquired?}
    LOCK -->|No| SELECT
    LOCK -->|Yes| OTP[Verify OTP]
    
    OTP --> PAYMENT[Process Payment]
    PAYMENT --> CONFIRM[Confirm Booking]
    CONFIRM --> TICKET[Issue Ticket]
    TICKET --> END([End])
    
    SELECT -.->|5 min<br/>timeout| EXPIRE[Expire]
    EXPIRE -.-> SELECT
    
    style LOCK fill:#fff9c4
    style SELECT fill:#ffcdd2
    style CONFIRM fill:#c8e6c9
    style END fill:#81c784
```

---

## Which One to Use?

- **Option 1**: Simplest - just 6 boxes
- **Option 2**: Shows services involved
- **Option 3**: Timeline format (good for presentations)
- **Option 4**: User experience focused
- **Option 5**: Architecture overview
- **Option 6**: Most visual with emojis
- **Option 7**: Data flow perspective
- **Option 8**: Clean and minimal

Choose based on your audience:
- **For judges**: Option 2, 5, or 6
- **For presentation**: Option 3 or 6
- **For documentation**: Option 7 or 8
- **For quick overview**: Option 1
