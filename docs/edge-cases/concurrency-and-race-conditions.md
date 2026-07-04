# Concurrency and Race Conditions

Managing simultaneous resource modifications.

## Maintenance Ticket Double Assign
- **Scenario**: Two vendors accept work order at same time.
- **Mitigation**: MongoDB atomic update transaction: `findOneAndUpdate({ _id: ticket_id, status: "OPEN" }, { $set: { status: "ASSIGNED", vendor_id: vendor_id } })`.
