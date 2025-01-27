#!/bin/bash

BASE_DIR="$HOME/.local_adventure"
DEFAULT_CUSTOMER_JSON='{"type": "", "name": "", "slug": "", "salesforceId": "", "enterpriseId": "", "zendeskOrgs": "", "expertAdventureUrl": "", "premiumPlusIssueUrl": "", "premiumSupportPageUrl": "", "healthChecksUrl": "", "customerFeedbackUrl": ""}'
DEFAULT_TICKET_JSON='{"ticketId": "", "status": "", "createdAt": "", "updatedAt": "", "description": ""}'

categories=("primary" "secondary" "tertiary")
primary_customers=("☕️ Starbucks" "🕹️ Discord" "🚗 Aurora" "🚀 Rocket")
secondary_customers=("💊 Prime" "📈 DRW" "❄️ Snowflake")
tertiary_customers=("🍎 Apple" "💾 IBM")

generate_ticket_id() { echo $((RANDOM % 90000 + 10000)); }

for category in "${categories[@]}"; do
    CATEGORY_DIR="$BASE_DIR/$category"
    CX_DIR="$CATEGORY_DIR/cx"
    TX_DIR="$CATEGORY_DIR/tx"
    OPEN_DIR="$TX_DIR/open"
    CLOSED_DIR="$TX_DIR/closed"

    mkdir -p "$CX_DIR" "$OPEN_DIR" "$CLOSED_DIR"

    case "$category" in
        "primary") customers=("${primary_customers[@]}") ;;
        "secondary") customers=("${secondary_customers[@]}") ;;
        "tertiary") customers=("${tertiary_customers[@]}") ;;
    esac

    for customer in "${customers[@]}"; do
        CUSTOMER_DIR="$CX_DIR/$customer"
        mkdir -p "$CUSTOMER_DIR"
        echo "$DEFAULT_CUSTOMER_JSON" > "$CUSTOMER_DIR/customer.json"
    done

    for i in {1..10}; do
        TICKET_ID=$(generate_ticket_id)
        STATUS_DIR=$([[ $((i % 2)) -eq 0 ]] && echo "$OPEN_DIR" || echo "$CLOSED_DIR")
        TICKET_DIR="$STATUS_DIR/$TICKET_ID"
        mkdir -p "$TICKET_DIR"
        echo "$DEFAULT_TICKET_JSON" | jq --arg ticketId "$TICKET_ID" --arg status $([[ $STATUS_DIR == "$OPEN_DIR" ]] && echo "open" || echo "closed") \
            '.ticketId = $ticketId | .status = $status' > "$TICKET_DIR/ticket.json"
    done

done

echo "Seeding completed successfully!"
