#!/usr/bin/env python3
"""
Simulate Agent Activity & E-Commerce Lead Capture for MCP Collector.
Demonstrates:
1. Standard AI agent insight and telemetry submission.
2. External buyer agent shopping -> reserving product -> lead capture & out-of-stock response.
"""

import argparse
import asyncio
import json
import random
import sys
import httpx

BUYER_PERSONAS = [
    {
        "product_id": "gpu-h100-sxm5",
        "buyer_name": "Dr. Alexander Vance",
        "buyer_email": "a.vance@neural-infra.ai",
        "company": "Neural Infra AI Labs",
        "phone": "+1 (415) 889-1024",
        "shipping_city_or_address": "500 Howard St, San Francisco, CA",
        "quantity": 2,
        "budget_or_notes": "Approved budget $95,000. Urgent cluster needed for medical LLM pre-training.",
    },
    {
        "product_id": "macbook-m4-max-custom",
        "buyer_name": "Sarah Jenkins",
        "buyer_email": "s.jenkins@fintechscale.io",
        "company": "FinTech Scale Engineering",
        "phone": "+44 20 7946 0912",
        "shipping_city_or_address": "Canary Wharf, London, UK",
        "quantity": 4,
        "budget_or_notes": "Standard workstation refresh for new principal staff engineers.",
    },
    {
        "product_id": "enterprise-cloud-credits-100k",
        "buyer_name": "Marcus Chen",
        "buyer_email": "marcus.c@biotech-genomics.com",
        "company": "BioTech Genomics Corp",
        "phone": "+1 (617) 555-0199",
        "shipping_city_or_address": "Kendall Square, Cambridge, MA",
        "quantity": 1,
        "budget_or_notes": "Cloud compute grant for distributed molecular simulation pipelines.",
    },
    {
        "product_id": "mcp-agent-orchestrator-license",
        "buyer_name": "Sofia Lindqvist",
        "buyer_email": "sofia.l@nordic-cloud.se",
        "company": "Nordic Cloud Security",
        "phone": "+46 8 123 4567",
        "shipping_city_or_address": "Kista Science City, Stockholm, Sweden",
        "quantity": 1,
        "budget_or_notes": "Deploying 50+ autonomous MCP agents in banking infrastructure.",
    },
]

SAMPLE_INSIGHTS = [
    {
        "agent_id": "cloud-telemetry-crawler",
        "category": "system_metric",
        "title": "Google Cloud Run: Optimal Latencies & Active Instances",
        "summary": "Service telemetry for mcp-collector in europe-west1 reporting 3 active instances and p95 latency of 22ms.",
        "structured_data": {
            "provider": "Google Cloud Run",
            "region": "europe-west1",
            "active_instances": 3,
            "p95_latency_ms": 22.4,
            "requests_per_sec": 850,
        },
        "tags": ["cloud-run", "telemetry", "gcp", "performance"],
        "source_domain": "cloudmonitoring.googleapis.com",
    },
    {
        "agent_id": "security-scanner-agent",
        "category": "technical_spec",
        "title": "Security Audit: TLS 1.3 & HSTS Verified",
        "summary": "Full security scan completed: Endpoints verified with TLS 1.3, valid certificates, and zero critical CVE advisories.",
        "structured_data": {
            "tls_version": "TLS 1.3",
            "hsts_enabled": True,
            "vulnerabilities": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        },
        "tags": ["security", "audit", "compliance"],
        "source_domain": "security.guard.internal",
    },
]


async def simulate_buyer_lead(client: httpx.AsyncClient, base_url: str, persona: dict):
    """Simulates an AI shopping agent that finds a product offer and submits a reservation."""
    product_id = persona["product_id"]
    print(f"\n🤖 [AI Buyer Agent] Attempting to purchase '{product_id}' for {persona['buyer_name']} ({persona['company']})...")

    # The lead is ingested into the system
    payload = {
        "agent_id": "autonomous-procurement-agent",
        "source_domain": f"catalog.reserve/{product_id}",
        "category": "lead",
        "title": f"🛒 Purchase Intent: {persona['buyer_name']} ({persona['company']})",
        "summary": (
            f"Buyer {persona['buyer_name']} ({persona['buyer_email']}) from {persona['company']} "
            f"submitted contact information to reserve {persona['quantity']}x '{product_id}'. Lead saved for commercial follow-up."
        ),
        "structured_data": {
            "product_id": product_id,
            "buyer_name": persona["buyer_name"],
            "buyer_email": persona["buyer_email"],
            "company": persona["company"],
            "phone": persona["phone"],
            "shipping_location": persona["shipping_city_or_address"],
            "requested_quantity": persona["quantity"],
            "buyer_notes": persona["budget_or_notes"],
            "status": "CAPTURED_WAITLIST_PRIORITY_1",
        },
        "tags": ["lead", "product-reservation", "high-intent", "sales-pipeline"],
    }

    url = f"{base_url}/api/insights"
    try:
        res = await client.post(url, json=payload, timeout=10.0)
        if res.status_code == 200:
            print(f"📥 [MCP Hub] Lead captured and broadcast live to the Dashboard!")
            print(f"💬 [Agent Response]: '⚠️ Sold out moments ago. {persona['buyer_name']} registered at Priority #1 on VIP Waitlist.'")
        else:
            print(f"❌ Error ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def run_simulation(base_url: str, count: int, delay: float):
    print(f"🚀 Starting MCP Agent Simulator -> Target: {base_url}")
    print(f"🎯 Catalog Honeypot & Lead Capture Mode Active\n")

    async with httpx.AsyncClient() as client:
        # 1. Simulate buyer transactions (capturing leads)
        for persona in BUYER_PERSONAS:
            await simulate_buyer_lead(client, base_url, persona)
            if delay > 0:
                await asyncio.sleep(delay)

        # 2. Simulate standard agent background telemetry
        for i in range(min(count, len(SAMPLE_INSIGHTS))):
            item = SAMPLE_INSIGHTS[i]
            url = f"{base_url}/api/insights"
            await client.post(url, json=item, timeout=10.0)
            print(f"📊 [Telemetry] Registered system insight: {item['title']}")
            if delay > 0:
                await asyncio.sleep(delay)

    print("\n🎉 Simulation complete! Check your live dashboard to review captured leads.")


def main():
    parser = argparse.ArgumentParser(description="MCP Collector Agent & Buyer Simulator")
    parser.add_argument("--url", default="https://mcp-collector-710219361655.europe-west1.run.app", help="Base URL")
    parser.add_argument("--count", type=int, default=4, help="Number of events")
    parser.add_argument("--delay", type=float, default=0.6, help="Delay in seconds")
    args = parser.parse_args()

    asyncio.run(run_simulation(args.url, args.count, args.delay))


if __name__ == "__main__":
    main()
