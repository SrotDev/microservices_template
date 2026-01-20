# Train Ticketing System - Architecture Diagrams

## 1. Complete System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        FE[Frontend<br/>React/HTML+JS<br/>Port: 3000]
    end

    subgraph "API Gateway Layer"
        GW[API Gateway<br/>Nginx<br/>Port: 80]
    end

    subgraph "Microservices Layer"
        AUTH[Auth Service<br/>Flask<br/>Port: 5001]
        TRAIN[Train Service<br/>Flask<br/>Port: 5002]
        BOOK1[Booking Service 1<br/>Flask<br/>Port: 5003]
        BOOK2[Booking Service 2<br/>Flask<br/>Port: 5003]
        BOOK3[Booking Service 3<br/>Flask<br/>Port: 5003]
        PAY[Payment Service<br/>Flask<br/>Port: 5004]
        NOTIF[Notification Service<br/>Flask<br/>Port: 5005]
    end

    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Port: 5432)]
        REDIS[(Redis<br/>Port: 6379)]
        MQ[RabbitMQ<br/>Port: 5672]
    end

    subgraph "Monitoring Layer"
        PROM[Prometheus<br/>Port: 9090]
        GRAF[Grafana<br/>Port: 3001]
    end

    %% Client to Gateway
    FE -->|HTTP/HTTPS| GW

    %% Gateway to Services
    GW -->|/api/auth/*| AUTH
    GW -->|/api/trains/*| TRAIN
    GW -->|/api/bookings/*<br/>Load Balanced| BOOK1
    GW -->|/api/bookings/*<br/>Load Balanced| BOOK2
    GW -->|/api/bookings/*<br/>Load Balanced| BOOK3
    GW -->|/api/payments/*| PAY

    %% Services to Data Layer
    AUTH -->|User Data| PG
    AUTH -->|JWT Cache| REDIS
    TRAIN -->|Train/Seat Data| PG
    TRAIN -->|Query Cache| REDIS
    BOOK1 -->|Booking Data| PG
    BOOK1 -->|Seat Locks| REDIS
    BOOK1 -->|Publish Events| MQ
    BOOK2 -->|Booking Data| PG
    BOOK2 -->|Seat Locks| REDIS
    BOOK2 -->|Publish Events| MQ
    BOOK3 -->|Booking Data| PG
    BOOK3 -->|Seat Locks| REDIS
    BOOK3 -->|Publish Events| MQ
    PAY -->|Payment Data| PG
    PAY -->|Publish Events| MQ
    NOTIF -->|Consume Events| MQ

    %% Monitoring
    AUTH -.->|Metrics| PROM
    TRAIN -.->|Metrics| PROM
    BOOK1 -.->|Metrics| PROM
    BOOK2 -.->|Metrics| PROM
    BOOK3 -.->|Metrics| PROM
    PAY -.->|Metrics| PROM
    NOTIF -.->|Metrics| PROM
    GW -.->|Metrics| PROM
    PROM -->|Data Source| GRAF

    style FE fill:#e1f5ff
    style GW fill:#fff4e6
    style AUTH fill:#f3e5f5
    style TRAIN fill:#f3e5f5
    style BOOK1 fill:#ffebee
    style BOOK2 fill:#ffebee
    style BOOK3 fill:#ffebee
    style PAY fill:#f3e5f5
    style NOTIF fill:#f3e5f5
    style PG fill:#e8f5e9
    style REDIS fill:#e8f5e9
    style MQ fill:#e8f5e9
    style PROM fill:#fff3e0
    style GRAF fill:#fff3e0
```

## 2. Complete Booking Journey - Simple Flow

```mermaid
graph LR
    subgraph "Phase 1: Authentication"
        A1[User Login] --> A2[Verify Credentials]
        A2 --> A3[Generate JWT Token]
        A3 --> A4[User Authenticated]
    end
    
    subgraph "Phase 2: Search & Browse"
        B1[Search Trains] --> B2[Check Cache]
        B2 --> B3[Return Train List]
        B3 --> B4[Display Seats]
    end
    
    subgraph "Phase 3: Seat Selection - CRITICAL"
        C1[Click Seat] --> C2{Seat Available?}
        C2 -->|No| C3[Show Error]
        C2 -->|Yes| C4[Lock Seat in Redis]
        C4 --> C5[Create Booking]
        C5 --> C6[Start 5-min Timer]
    end
    
    subgraph "Phase 4: Verification"
        D1[Enter OTP] --> D2[Verify OTP]
        D2 --> D3[Update Booking Status]
    end
    
    subgraph "Phase 5: Payment"
        E1[Enter Payment Info] --> E2[Process Payment]
        E2 --> E3[Save Payment Record]
        E3 --> E4[Publish Event to Queue]
    end
    
    subgraph "Phase 6: Confirmation"
        F1[Confirm Booking] --> F2[Update Seat Status]
        F2 --> F3[Release Redis Lock]
        F3 --> F4[Generate Ticket]
        F4 --> F5[Send Notification]
    end
    
    A4 --> B1
    B4 --> C1
    C3 --> B4
    C6 --> D1
    D3 --> E1
    E4 --> F1
    F5 --> G[Booking Complete]
    
    C6 -.->|Timeout| T1[Auto-Release Lock]
    T1 -.-> B4
    
    style C4 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style C5 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style C6 fill:#ffcdd2,stroke:#c62828,stroke-width:3px
    style F3 fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style G fill:#81c784,stroke:#1b5e20,stroke-width:3px
```

## 2A. Complete Booking Journey - Linear Timeline

```mermaid
graph TD
    START([👤 User Starts Journey]) --> STEP1
    
    STEP1[🔐 Step 1: Login<br/>POST /api/auth/login<br/>Response: JWT Token] --> STEP2
    
    STEP2[🔍 Step 2: Search Trains<br/>GET /api/trains/search<br/>Response: Available Trains] --> STEP3
    
    STEP3[💺 Step 3: Select Seat<br/>POST /api/bookings/seats/select<br/>⚠️ CRITICAL: Redis Lock Acquired<br/>Response: Booking ID + 5 min timer] --> STEP4
    
    STEP4[📱 Step 4: Verify OTP<br/>POST /api/bookings/verify-otp<br/>Response: OTP Confirmed] --> STEP5
    
    STEP5[💳 Step 5: Make Payment<br/>POST /api/payments/initiate<br/>Response: Payment Success] --> STEP6
    
    STEP6[✅ Step 6: Confirm Booking<br/>POST /api/bookings/confirm<br/>Actions:<br/>- Update seat status<br/>- Release Redis lock<br/>- Publish to RabbitMQ<br/>Response: Ticket Generated] --> STEP7
    
    STEP7[📧 Step 7: Send Notification<br/>Async via RabbitMQ<br/>Email confirmation sent] --> END
    
    END([🎉 Booking Complete])
    
    STEP3 -.->|⏱️ Timeout 5 min| TIMEOUT[❌ Lock Released<br/>Booking Cancelled]
    TIMEOUT -.-> STEP2
    
    style START fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style STEP3 fill:#ffebee,stroke:#c62828,stroke-width:4px
    style STEP6 fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style END fill:#c8e6c9,stroke:#1b5e20,stroke-width:3px
    style TIMEOUT fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
```

## 2B. Complete Booking Journey (Detailed Flowchart)

```mermaid
flowchart TD
    START([User Opens Website]) --> LOGIN[User Enters Credentials]
    LOGIN --> AUTH_CHECK{Valid Credentials?}
    
    AUTH_CHECK -->|No| LOGIN_FAIL[Show Error Message]
    LOGIN_FAIL --> LOGIN
    AUTH_CHECK -->|Yes| JWT[Generate JWT Token]
    JWT --> CACHE_JWT[Cache JWT in Redis]
    CACHE_JWT --> DASHBOARD[Show Dashboard]
    
    DASHBOARD --> SEARCH[User Searches Trains<br/>From: Dhaka, To: Chittagong]
    SEARCH --> CHECK_CACHE{Train Data<br/>in Cache?}
    
    CHECK_CACHE -->|Yes| RETURN_CACHE[Return Cached Data]
    CHECK_CACHE -->|No| QUERY_DB[Query Database]
    QUERY_DB --> CACHE_RESULT[Cache Results<br/>TTL: 5 min]
    CACHE_RESULT --> RETURN_CACHE
    
    RETURN_CACHE --> DISPLAY_TRAINS[Display Available Trains]
    DISPLAY_TRAINS --> SELECT_TRAIN[User Selects Train]
    SELECT_TRAIN --> SHOW_SEATS[Show Seat Layout]
    
    SHOW_SEATS --> SELECT_SEAT[User Clicks on Seat]
    SELECT_SEAT --> LOCK_CHECK{Is Seat<br/>Locked?}
    
    LOCK_CHECK -->|Yes - Locked| SEAT_TAKEN[Show: Seat Already Taken]
    SEAT_TAKEN --> SHOW_SEATS
    
    LOCK_CHECK -->|No - Available| ACQUIRE_LOCK[Acquire Redis Lock<br/>Key: seat:123<br/>TTL: 300 sec]
    ACQUIRE_LOCK --> CREATE_BOOKING[Create Booking Record<br/>Status: PENDING]
    CREATE_BOOKING --> START_TIMER[Start 5-Minute Timer]
    START_TIMER --> SHOW_OTP[Show OTP Input Screen]
    
    SHOW_OTP --> ENTER_OTP[User Enters OTP]
    ENTER_OTP --> VERIFY_OTP{OTP Valid?}
    
    VERIFY_OTP -->|No| OTP_FAIL[Show Error]
    OTP_FAIL --> SHOW_OTP
    
    VERIFY_OTP -->|Yes| UPDATE_STATUS1[Update Booking<br/>Status: OTP_VERIFIED]
    UPDATE_STATUS1 --> SHOW_PAYMENT[Show Payment Page]
    
    SHOW_PAYMENT --> ENTER_PAYMENT[User Enters Payment Info]
    ENTER_PAYMENT --> PROCESS_PAYMENT[Process Payment<br/>Mock Gateway]
    PROCESS_PAYMENT --> PAYMENT_CHECK{Payment<br/>Success?}
    
    PAYMENT_CHECK -->|No| PAYMENT_FAIL[Show Payment Error]
    PAYMENT_FAIL --> SHOW_PAYMENT
    
    PAYMENT_CHECK -->|Yes| SAVE_PAYMENT[Save Payment Record]
    SAVE_PAYMENT --> PUBLISH_EVENT1[Publish: payment.success]
    PUBLISH_EVENT1 --> CONFIRM_BOOKING[Confirm Booking]
    
    CONFIRM_BOOKING --> UPDATE_SEAT[Update Seat Status: BOOKED]
    UPDATE_SEAT --> UPDATE_STATUS2[Update Booking<br/>Status: CONFIRMED]
    UPDATE_STATUS2 --> RELEASE_LOCK[Release Redis Lock]
    RELEASE_LOCK --> PUBLISH_EVENT2[Publish: booking.confirmed]
    PUBLISH_EVENT2 --> GENERATE_TICKET[Generate Ticket<br/>Booking Reference]
    
    GENERATE_TICKET --> SHOW_TICKET[Display Ticket to User]
    SHOW_TICKET --> SEND_EMAIL[Send Confirmation Email<br/>Async via RabbitMQ]
    SEND_EMAIL --> END([Booking Complete])
    
    %% Timeout Path
    START_TIMER -.->|5 min timeout| TIMEOUT[Timer Expires]
    TIMEOUT --> AUTO_RELEASE[Auto-Release Lock]
    AUTO_RELEASE --> CANCEL_BOOKING[Cancel Booking]
    CANCEL_BOOKING --> SEAT_AVAILABLE[Seat Available Again]
    
    style START fill:#e3f2fd
    style LOGIN fill:#e1f5ff
    style AUTH_CHECK fill:#fff9c4
    style DASHBOARD fill:#c8e6c9
    style SELECT_SEAT fill:#ffecb3
    style LOCK_CHECK fill:#fff9c4
    style ACQUIRE_LOCK fill:#ffcdd2
    style VERIFY_OTP fill:#fff9c4
    style PAYMENT_CHECK fill:#fff9c4
    style CONFIRM_BOOKING fill:#c8e6c9
    style SHOW_TICKET fill:#a5d6a7
    style END fill:#81c784
    style TIMEOUT fill:#ffab91
    style SEAT_TAKEN fill:#ef9a9a
```

## 2C. Complete Booking Journey (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> Anonymous: User Visits Site
    
    Anonymous --> Authenticated: Login Success
    Anonymous --> Anonymous: Login Failed
    
    Authenticated --> SearchingTrains: Search Trains
    SearchingTrains --> ViewingSeats: Select Train
    
    ViewingSeats --> SeatLocked: Click Available Seat
    ViewingSeats --> ViewingSeats: Seat Already Taken
    
    state SeatLocked {
        [*] --> PendingOTP: Lock Acquired (5 min)
        PendingOTP --> OTPVerified: Valid OTP
        PendingOTP --> PendingOTP: Invalid OTP
        PendingOTP --> [*]: Timeout (5 min)
    }
    
    SeatLocked --> ViewingSeats: Timeout/Cancel
    SeatLocked --> PendingPayment: OTP Verified
    
    state PendingPayment {
        [*] --> ProcessingPayment: Submit Payment
        ProcessingPayment --> PaymentSuccess: Payment OK
        ProcessingPayment --> ProcessingPayment: Payment Failed
    }
    
    PendingPayment --> ViewingSeats: Cancel
    PendingPayment --> BookingConfirmed: Payment Success
    
    state BookingConfirmed {
        [*] --> UpdatingDatabase: Confirm Booking
        UpdatingDatabase --> ReleasingLock: Update Seat
        ReleasingLock --> PublishingEvents: Release Redis Lock
        PublishingEvents --> GeneratingTicket: Publish to Queue
        GeneratingTicket --> [*]: Ticket Generated
    }
    
    BookingConfirmed --> TicketIssued: Booking Complete
    
    state TicketIssued {
        [*] --> SendingNotification: Send Email
        SendingNotification --> [*]: Email Sent
    }
    
    TicketIssued --> [*]: Journey Complete
    
    note right of SeatLocked
        Critical Section:
        Redis lock prevents
        double booking
    end note
    
    note right of BookingConfirmed
        Atomic operations:
        All or nothing
    end note
```

## 2D. Complete Booking Journey (Swimlane Diagram)

```mermaid
graph TB
    subgraph "User Actions"
        U1[Open Website]
        U2[Enter Login]
        U3[Search Trains]
        U4[Select Seat]
        U5[Enter OTP]
        U6[Enter Payment]
        U7[View Ticket]
    end
    
    subgraph "Frontend Layer"
        F1[Render Login Page]
        F2[Send Auth Request]
        F3[Display Trains]
        F4[Show Seat Map]
        F5[Show OTP Modal]
        F6[Show Payment Form]
        F7[Display Ticket]
    end
    
    subgraph "API Gateway"
        G1[Route to Auth]
        G2[Route to Train]
        G3[Route to Booking]
        G4[Route to Payment]
        G5[Load Balance]
    end
    
    subgraph "Business Logic"
        B1[Verify Credentials]
        B2[Query Trains]
        B3[Acquire Lock]
        B4[Verify OTP]
        B5[Process Payment]
        B6[Confirm Booking]
    end
    
    subgraph "Data Layer"
        D1[Check User DB]
        D2[Cache Train Data]
        D3[Lock Seat Redis]
        D4[Save Booking DB]
        D5[Save Payment DB]
        D6[Update Seat DB]
    end
    
    subgraph "Async Processing"
        A1[Publish Event]
        A2[Send Notification]
        A3[Log Activity]
    end
    
    U1 --> F1
    F1 --> U2
    U2 --> F2
    F2 --> G1
    G1 --> B1
    B1 --> D1
    D1 --> B1
    B1 --> G1
    G1 --> F2
    F2 --> U3
    
    U3 --> F3
    F3 --> G2
    G2 --> B2
    B2 --> D2
    D2 --> B2
    B2 --> G2
    G2 --> F3
    F3 --> F4
    F4 --> U4
    
    U4 --> F4
    F4 --> G3
    G3 --> G5
    G5 --> B3
    B3 --> D3
    D3 --> B3
    B3 --> D4
    D4 --> B3
    B3 --> G5
    G5 --> G3
    G3 --> F5
    F5 --> U5
    
    U5 --> F5
    F5 --> G3
    G3 --> B4
    B4 --> G3
    G3 --> F6
    F6 --> U6
    
    U6 --> F6
    F6 --> G4
    G4 --> B5
    B5 --> D5
    D5 --> B5
    B5 --> A1
    A1 --> A2
    B5 --> G4
    G4 --> G3
    G3 --> B6
    B6 --> D6
    D6 --> B6
    B6 --> A1
    A2 --> A3
    B6 --> G3
    G3 --> F7
    F7 --> U7
    
    style U4 fill:#ffcdd2
    style B3 fill:#ffcdd2
    style D3 fill:#ffcdd2
    style G5 fill:#fff9c4
    style A1 fill:#c8e6c9
    style A2 fill:#c8e6c9
```

## 3. Seat Locking Mechanism (Critical Component)

```mermaid
flowchart TD
    START([User Selects Seat]) --> CHECK{Check Redis Lock}
    
    CHECK -->|Lock Exists| FAIL[Return: Seat Unavailable]
    CHECK -->|No Lock| ACQUIRE[Acquire Redis Lock]
    
    ACQUIRE --> SETKEY[Set Key: seat:{id}<br/>Value: user_id<br/>TTL: 300 seconds]
    SETKEY --> CREATEBOOK[Create Booking Record<br/>Status: PENDING]
    CREATEBOOK --> RETURN[Return: Booking ID<br/>Timer: 5 minutes]
    
    RETURN --> WAIT{User Action?}
    
    WAIT -->|Complete Payment<br/>Within 5 min| CONFIRM[Confirm Booking]
    WAIT -->|Timeout<br/>5 minutes| EXPIRE[Redis Key Expires]
    WAIT -->|User Cancels| RELEASE[Manual Release Lock]
    
    CONFIRM --> UPDATEDB[Update Seat Status: BOOKED]
    UPDATEDB --> DELLOCK[Delete Redis Lock]
    DELLOCK --> SUCCESS([Booking Complete])
    
    EXPIRE --> AUTORELEASE[Seat Auto-Released]
    RELEASE --> AUTORELEASE
    AUTORELEASE --> AVAILABLE([Seat Available Again])
    
    FAIL --> END([End])
    
    style START fill:#e3f2fd
    style CHECK fill:#fff9c4
    style ACQUIRE fill:#c8e6c9
    style CONFIRM fill:#c8e6c9
    style FAIL fill:#ffcdd2
    style EXPIRE fill:#ffecb3
    style SUCCESS fill:#a5d6a7
    style AVAILABLE fill:#a5d6a7
```

## 4. Event-Driven Architecture (RabbitMQ)

```mermaid
graph LR
    subgraph "Publishers"
        BOOK[Booking Service]
        PAY[Payment Service]
    end

    subgraph "Message Broker"
        EX[Exchange:<br/>booking_events]
        Q1[Queue:<br/>payment_queue]
        Q2[Queue:<br/>notification_queue]
    end

    subgraph "Consumers"
        PAYC[Payment Service<br/>Consumer]
        NOTIF[Notification Service<br/>Consumer]
    end

    BOOK -->|booking.created| EX
    BOOK -->|booking.confirmed| EX
    PAY -->|payment.success| EX
    PAY -->|payment.failed| EX

    EX -->|Route| Q1
    EX -->|Route| Q2

    Q1 -->|Consume| PAYC
    Q2 -->|Consume| NOTIF

    style BOOK fill:#e1bee7
    style PAY fill:#e1bee7
    style EX fill:#fff9c4
    style Q1 fill:#c5cae9
    style Q2 fill:#c5cae9
    style PAYC fill:#b2dfdb
    style NOTIF fill:#b2dfdb
```

## 5. Database Schema (ER Diagram)

```mermaid
erDiagram
    USERS ||--o{ BOOKINGS : makes
    TRAINS ||--o{ COACHES : has
    COACHES ||--o{ SEATS : contains
    SEATS ||--o{ BOOKINGS : reserved_in
    BOOKINGS ||--|| PAYMENTS : has

    USERS {
        int id PK
        string email UK
        string password_hash
        string phone
        string name
        timestamp created_at
    }

    TRAINS {
        int id PK
        string name
        string route
        timestamp departure_time
        timestamp arrival_time
        string status
    }

    COACHES {
        int id PK
        int train_id FK
        string coach_number
        int total_seats
        string coach_type
    }

    SEATS {
        int id PK
        int coach_id FK
        string seat_number
        string status
        timestamp locked_until
        int locked_by FK
        decimal price
    }

    BOOKINGS {
        int id PK
        int user_id FK
        int seat_id FK
        string booking_reference UK
        string status
        timestamp created_at
        timestamp confirmed_at
        string passenger_name
        string passenger_phone
    }

    PAYMENTS {
        int id PK
        int booking_id FK
        decimal amount
        string payment_method
        string transaction_id
        string status
        timestamp created_at
        timestamp completed_at
    }
```

## 6. CI/CD Pipeline

```mermaid
flowchart TD
    START([Developer Push/PR]) --> TRIGGER[GitHub Actions Triggered]
    
    TRIGGER --> DETECT[Detect Changed Services<br/>paths-filter action]
    
    DETECT --> PARALLEL{Run Tests in Parallel}
    
    PARALLEL -->|Auth Changed| T1[Test Auth Service]
    PARALLEL -->|Train Changed| T2[Test Train Service]
    PARALLEL -->|Booking Changed| T3[Test Booking Service]
    PARALLEL -->|Payment Changed| T4[Test Payment Service]
    PARALLEL -->|Notification Changed| T5[Test Notification Service]
    
    T1 --> BUILD1[Build Docker Image]
    T2 --> BUILD2[Build Docker Image]
    T3 --> BUILD3[Build Docker Image]
    T4 --> BUILD4[Build Docker Image]
    T5 --> BUILD5[Build Docker Image]
    
    BUILD1 --> PUSH1[Push to Registry]
    BUILD2 --> PUSH2[Push to Registry]
    BUILD3 --> PUSH3[Push to Registry]
    BUILD4 --> PUSH4[Push to Registry]
    BUILD5 --> PUSH5[Push to Registry]
    
    PUSH1 --> MERGE{Merged to Main?}
    PUSH2 --> MERGE
    PUSH3 --> MERGE
    PUSH4 --> MERGE
    PUSH5 --> MERGE
    
    MERGE -->|Yes| CD[CD Pipeline Triggered]
    MERGE -->|No| ENDPR([End - PR Complete])
    
    CD --> DEPLOY[Deploy Changed Services]
    DEPLOY --> HEALTH[Health Check]
    
    HEALTH -->|Pass| ROUTE[Route Traffic]
    HEALTH -->|Fail| ROLLBACK[Rollback]
    
    ROUTE --> SUCCESS([Deployment Complete])
    ROLLBACK --> ALERT[Alert Team]
    ALERT --> ENDFAIL([End - Failed])
    
    style START fill:#e3f2fd
    style TRIGGER fill:#fff9c4
    style DETECT fill:#f3e5f5
    style PARALLEL fill:#e1bee7
    style MERGE fill:#fff9c4
    style CD fill:#c8e6c9
    style SUCCESS fill:#a5d6a7
    style ROLLBACK fill:#ffcdd2
    style ENDFAIL fill:#ffcdd2
```

## 7. Load Testing Architecture

```mermaid
graph TB
    subgraph "Load Testing Infrastructure"
        LT[Locust Master<br/>Separate VM]
        W1[Locust Worker 1]
        W2[Locust Worker 2]
        W3[Locust Worker 3]
    end

    subgraph "Target System"
        LB[Load Balancer]
        GW[API Gateway]
        
        subgraph "Services"
            B1[Booking 1]
            B2[Booking 2]
            B3[Booking 3]
        end
        
        REDIS[(Redis)]
        DB[(PostgreSQL)]
    end

    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
    end

    LT --> W1
    LT --> W2
    LT --> W3

    W1 -->|HTTP Requests| LB
    W2 -->|HTTP Requests| LB
    W3 -->|HTTP Requests| LB

    LB --> GW
    GW --> B1
    GW --> B2
    GW --> B3

    B1 --> REDIS
    B2 --> REDIS
    B3 --> REDIS
    B1 --> DB
    B2 --> DB
    B3 --> DB

    B1 -.->|Metrics| PROM
    B2 -.->|Metrics| PROM
    B3 -.->|Metrics| PROM
    REDIS -.->|Metrics| PROM
    DB -.->|Metrics| PROM

    PROM --> GRAF
    LT -.->|Results| GRAF

    style LT fill:#ffecb3
    style W1 fill:#fff9c4
    style W2 fill:#fff9c4
    style W3 fill:#fff9c4
    style LB fill:#e1bee7
    style GW fill:#e1bee7
    style B1 fill:#ffcdd2
    style B2 fill:#ffcdd2
    style B3 fill:#ffcdd2
    style PROM fill:#c8e6c9
    style GRAF fill:#c8e6c9
```

## 8. Deployment Architecture (Cloud)

```mermaid
graph TB
    subgraph "Internet"
        USER[Users]
    end

    subgraph "Cloud Provider (AWS/GCP/DigitalOcean)"
        subgraph "Load Balancer"
            ALB[Application Load Balancer<br/>Public IP]
        end

        subgraph "Container Orchestration (Docker Swarm/K8s)"
            subgraph "Node 1"
                GW1[API Gateway]
                AUTH1[Auth Service]
                BOOK1[Booking Service]
            end

            subgraph "Node 2"
                TRAIN1[Train Service]
                BOOK2[Booking Service]
                PAY1[Payment Service]
            end

            subgraph "Node 3"
                BOOK3[Booking Service]
                NOTIF1[Notification Service]
                PROM[Prometheus]
            end
        end

        subgraph "Managed Services"
            RDS[(Managed PostgreSQL<br/>Multi-AZ)]
            ELASTICACHE[(Managed Redis<br/>Cluster)]
            MQ_MANAGED[Managed RabbitMQ<br/>CloudAMQP]
        end

        subgraph "Monitoring"
            GRAF[Grafana<br/>Separate Instance]
        end

        subgraph "Storage"
            S3[Object Storage<br/>Logs/Backups]
        end
    end

    USER -->|HTTPS| ALB
    ALB --> GW1

    GW1 --> AUTH1
    GW1 --> TRAIN1
    GW1 --> BOOK1
    GW1 --> BOOK2
    GW1 --> BOOK3
    GW1 --> PAY1

    AUTH1 --> RDS
    TRAIN1 --> RDS
    BOOK1 --> RDS
    BOOK2 --> RDS
    BOOK3 --> RDS
    PAY1 --> RDS

    BOOK1 --> ELASTICACHE
    BOOK2 --> ELASTICACHE
    BOOK3 --> ELASTICACHE
    AUTH1 --> ELASTICACHE

    BOOK1 --> MQ_MANAGED
    BOOK2 --> MQ_MANAGED
    BOOK3 --> MQ_MANAGED
    PAY1 --> MQ_MANAGED
    NOTIF1 --> MQ_MANAGED

    PROM --> GRAF
    AUTH1 -.->|Metrics| PROM
    TRAIN1 -.->|Metrics| PROM
    BOOK1 -.->|Metrics| PROM
    BOOK2 -.->|Metrics| PROM
    BOOK3 -.->|Metrics| PROM
    PAY1 -.->|Metrics| PROM
    NOTIF1 -.->|Metrics| PROM

    GW1 -.->|Logs| S3
    AUTH1 -.->|Logs| S3
    TRAIN1 -.->|Logs| S3

    style USER fill:#e3f2fd
    style ALB fill:#fff9c4
    style GW1 fill:#e1bee7
    style BOOK1 fill:#ffcdd2
    style BOOK2 fill:#ffcdd2
    style BOOK3 fill:#ffcdd2
    style RDS fill:#c8e6c9
    style ELASTICACHE fill:#c8e6c9
    style MQ_MANAGED fill:#c8e6c9
    style PROM fill:#b2dfdb
    style GRAF fill:#b2dfdb
```

## 9. Monitoring Dashboard Layout

```mermaid
graph TB
    subgraph "Grafana Dashboard"
        subgraph "Row 1: System Health"
            M1[CPU Usage<br/>All Services]
            M2[Memory Usage<br/>All Services]
            M3[Network I/O<br/>All Services]
        end

        subgraph "Row 2: Application Metrics"
            M4[Request Rate<br/>req/sec]
            M5[Response Time<br/>p50, p95, p99]
            M6[Error Rate<br/>4xx, 5xx]
        end

        subgraph "Row 3: Business Metrics"
            M7[Seat Selections<br/>per minute]
            M8[Booking Success Rate<br/>percentage]
            M9[Active Users<br/>concurrent]
        end

        subgraph "Row 4: Database & Cache"
            M10[DB Connections<br/>active/idle]
            M11[Query Duration<br/>avg/max]
            M12[Redis Hit Rate<br/>percentage]
        end

        subgraph "Row 5: Service-Specific"
            M13[Booking Service<br/>Lock Acquisitions]
            M14[Payment Service<br/>Transactions]
            M15[Queue Depth<br/>RabbitMQ]
        end
    end

    style M1 fill:#ffecb3
    style M2 fill:#ffecb3
    style M3 fill:#ffecb3
    style M4 fill:#e1bee7
    style M5 fill:#e1bee7
    style M6 fill:#e1bee7
    style M7 fill:#c8e6c9
    style M8 fill:#c8e6c9
    style M9 fill:#c8e6c9
    style M10 fill:#b3e5fc
    style M11 fill:#b3e5fc
    style M12 fill:#b3e5fc
    style M13 fill:#f8bbd0
    style M14 fill:#f8bbd0
    style M15 fill:#f8bbd0
```

## 10. Scalability Strategy

```mermaid
flowchart TD
    START([Traffic Increase Detected]) --> MONITOR{Monitor Metrics}
    
    MONITOR -->|CPU > 70%| SCALE1[Auto-Scale Booking Service]
    MONITOR -->|Memory > 80%| SCALE2[Scale Database Connections]
    MONITOR -->|Queue Depth > 1000| SCALE3[Scale Notification Service]
    MONITOR -->|Redis Hit Rate < 80%| SCALE4[Increase Cache Size]
    
    SCALE1 --> ADD1[Add Booking Service Replicas<br/>3 → 5 → 10]
    SCALE2 --> ADD2[Increase Connection Pool<br/>10 → 20 → 50]
    SCALE3 --> ADD3[Add Notification Workers<br/>1 → 3 → 5]
    SCALE4 --> ADD4[Increase Redis Memory<br/>1GB → 2GB → 4GB]
    
    ADD1 --> LB1[Load Balancer<br/>Distributes Traffic]
    ADD2 --> OPT1[Optimize Queries<br/>Add Indexes]
    ADD3 --> MQ1[RabbitMQ<br/>Distributes Messages]
    ADD4 --> CACHE1[Cache More Data<br/>Longer TTL]
    
    LB1 --> CHECK{Performance OK?}
    OPT1 --> CHECK
    MQ1 --> CHECK
    CACHE1 --> CHECK
    
    CHECK -->|Yes| SUCCESS([System Stable])
    CHECK -->|No| ALERT[Alert Team<br/>Manual Intervention]
    
    ALERT --> MANUAL[Manual Optimization:<br/>- Database Sharding<br/>- Read Replicas<br/>- CDN for Static Assets]
    
    MANUAL --> SUCCESS
    
    style START fill:#e3f2fd
    style MONITOR fill:#fff9c4
    style SCALE1 fill:#ffcdd2
    style SCALE2 fill:#e1bee7
    style SCALE3 fill:#c5cae9
    style SCALE4 fill:#b2dfdb
    style SUCCESS fill:#c8e6c9
    style ALERT fill:#ffab91
```

---

## Usage Instructions

1. **For Presentation**: Copy the relevant mermaid diagrams into your slides or use tools like:
   - Mermaid Live Editor: https://mermaid.live/
   - Draw.io with Mermaid plugin
   - VS Code with Mermaid preview extension

2. **For Documentation**: Include these diagrams in your README.md or ARCHITECTURE.md

3. **For Judges**: These diagrams clearly show:
   - System architecture and component interactions
   - Data flow and business logic
   - Scalability and resilience strategies
   - Monitoring and observability approach

4. **Customization**: Adjust colors, add/remove components based on your actual implementation
