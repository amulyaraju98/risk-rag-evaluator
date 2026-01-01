# SOP 002: Transaction Monitoring & Fraud Detection Rules

**Company:** ApexPay  
**Version:** 1.0  
**Owner:** Fraud Prevention Team  

## Purpose
Describe how to detect unusual merchant activity and prevent fraudulent transactions in real time.

---

## Daily Velocity Limits
| Risk Level | Max Value/Day | Max Txns/Day |
|-------------|---------------|--------------|
| Low 🟢 | $50 000 | 1000 |
| Medium 🟡 | $100 000 | 2000 |
| High 🔴 | $10 000 | 500 |

---

## Red Flag Indicators 
- **Velocity Spike:** >150 % of 30‑day avg → FLAG  
- **Txn Count Surge:** >200 % of avg → FLAG  
- **Geo Anomaly:** sudden multi‑country logins or TXNs  
- **Round Amounts:** frequent $1 000 / $5 000 payments  
- **Odd Hours:** bursts between 12–4 AM  
- **Circular Flow:** A → B → A pattern  
- **Refund Abuse:** >30 % refund ratio in 7 days  

---

## Response Levels
### Tier 1 – Yellow  (Minor)
- Auto email alert to merchant  
- 24 h monitoring increase  
- No blocking

### Tier 2 – Orange  (Serious)
- Analyst manual review + merchant contact  
- Reduce limits by 50 %  
- Escalate if no response in 48 h

### Tier 3 – Red  (Critical)
- Immediate hold on transactions  
- Executive fraud review  
- Full investigation + possible suspension  

---

## Monitoring Tools
- Real‑time dashboard  
- Automated alerts (AI‑based models)  
- Manual review queues  
- Data visualization for patterns  

---

## Reporting
All flagged incidents → monthly fraud summary to RBI compliance desk.
