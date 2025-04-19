static_rules:
  - id: check_status_active
    description: "Static config item must have status as 'active'"
    field: status
    expected: "active"
    level: error

  - id: check_required_name
    description: "Static config item must have a name"
    field: name
    required: true
    level: warning

transactional_rules:
  - id: check_positive_amount
    description: "Transaction amount must be greater than 0"
    field: amount
    operator: ">"
    value: 0
    level: error

  - id: check_valid_status
    description: "Transaction status must be completed or pending"
    field: status
    allowed_values: ["completed", "pending"]
    level: error

  - id: check_timestamp_present
    description: "Transaction must have a timestamp"
    field: timestamp
    required: true
    level: warning
