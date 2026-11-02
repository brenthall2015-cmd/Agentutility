from decimal import Decimal, ROUND_HALF_UP
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from security import require_api_key

app = FastAPI(title="AgentUtility", version="0.2.0", description="Private beta. No payment processing enabled.")
def D(x): return Decimal(str(x))
def money(x): return str(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

class Job(BaseModel):
    labor_hours: float = Field(ge=0, le=100000)
    labor_rate: float = Field(ge=0, le=1000000)
    materials: float = Field(ge=0, le=100000000)
    subcontractors: float = Field(default=0, ge=0, le=100000000)
    other_costs: float = Field(default=0, ge=0, le=100000000)
    target_margin: float = Field(ge=0, lt=1)

class ChangeOrder(Job):
    change_order_id: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=2000)
    tax_rate: float = Field(default=0, ge=0, le=1)

class InvoiceLine(BaseModel):
    description: str = Field(min_length=1, max_length=500)
    quantity: float = Field(ge=0, le=1000000)
    unit_price: float = Field(ge=0, le=100000000)
    stated_total: float = Field(ge=0, le=1000000000)

class Invoice(BaseModel):
    lines: List[InvoiceLine] = Field(min_length=1, max_length=200)
    stated_subtotal: float = Field(ge=0, le=100000000000)
    tax_rate: float = Field(default=0, ge=0, le=1)
    stated_tax: float = Field(default=0, ge=0, le=100000000000)
    stated_total: float = Field(ge=0, le=100000000000)

@app.get("/health")
def health(): return {"status":"ok","payments_enabled":False}

def job_result(d):
    cost = D(d.labor_hours)*D(d.labor_rate)+D(d.materials)+D(d.subcontractors)+D(d.other_costs)
    quote = cost/(1-D(d.target_margin))
    return {"cost":money(cost),"recommended_price":money(quote),"gross_profit":money(quote-cost)}

@app.post("/v1/job-pricing", dependencies=[Depends(require_api_key)])
def job_pricing(data:Job): return job_result(data)

@app.post("/v1/change-order", dependencies=[Depends(require_api_key)])
def change_order(data:ChangeOrder):
    result=job_result(data)
    subtotal=D(result["recommended_price"])
    tax=subtotal*D(data.tax_rate)
    return {"change_order_id":data.change_order_id,"description":data.description,**result,"tax":money(tax),"customer_total":money(subtotal+tax),"note":"Verify applicable taxes locally."}

@app.post("/v1/invoice-check", dependencies=[Depends(require_api_key)])
def invoice_check(data:Invoice):
    subtotal=Decimal("0")
    mismatches=[]
    for i,line in enumerate(data.lines,1):
        expected=(D(line.quantity)*D(line.unit_price)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        subtotal+=expected
        if abs(expected-D(line.stated_total))>Decimal("0.01"):
            mismatches.append({"line":i,"expected":money(expected),"stated":money(D(line.stated_total))})
    tax=(subtotal*D(data.tax_rate)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
    for field,expected,stated in [("subtotal",subtotal,data.stated_subtotal),("tax",tax,data.stated_tax),("total",subtotal+tax,data.stated_total)]:
        if abs(expected-D(stated))>Decimal("0.01"):
            mismatches.append({"field":field,"expected":money(expected),"stated":money(D(stated))})
    return {"valid":not mismatches,"expected_subtotal":money(subtotal),"expected_tax":money(tax),"expected_total":money(subtotal+tax),"mismatches":mismatches,"note":"Arithmetic checks only; not authenticity or legal validation."}
