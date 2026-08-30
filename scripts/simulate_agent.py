#!/usr/bin/env python3
"""
Simulate Agent Activity & E-Commerce Lead Capture for MCP Collector.
Demonstrates:
1. Standard AI agent insight submission.
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
        "buyer_name": "Dr. Alejandro Vidal",
        "buyer_email": "a.vidal@neural-infra.eu",
        "company": "Neural Infra AI Labs",
        "phone": "+34 622 889 102",
        "shipping_city_or_address": "Paseo de la Castellana 95, Madrid",
        "quantity": 2,
        "budget_or_notes": "Presupuesto aprobado €95,000. Urgente para entrenamiento de modelos LLM médicos.",
    },
    {
        "product_id": "macbook-m4-max-custom",
        "buyer_name": "Lucía Morales",
        "buyer_email": "lucia.morales@fintechscale.io",
        "company": "FinTech Scale Engineering",
        "phone": "+34 611 345 678",
        "shipping_city_or_address": "Barcelona Tech City, Pier 01",
        "quantity": 4,
        "budget_or_notes": "Equipamiento para nuevos ingenieros senior de arquitectura.",
    },
    {
        "product_id": "enterprise-cloud-credits-100k",
        "buyer_name": "Javier Sanz",
        "buyer_email": "j.sanz@biotech-solutions.es",
        "company": "BioTech Solutions SL",
        "phone": "+34 655 123 987",
        "shipping_city_or_address": "Valencia Innovation Hub",
        "quantity": 1,
        "budget_or_notes": "Créditos para cluster de simulación genómica.",
    },
    {
        "product_id": "mcp-agent-orchestrator-license",
        "buyer_name": "Sofia Kova",
        "buyer_email": "sofia.k@nordic-cloud.com",
        "company": "Nordic Cloud Services",
        "phone": "+46 8 123 4567",
        "shipping_city_or_address": "Stockholm Tech Park",
        "quantity": 1,
        "budget_or_notes": "Buscando integración de 50+ agentes MCP en red bancaria.",
    },
]

SAMPLE_INSIGHTS = [
    {
        "agent_id": "cloud-telemetry-crawler",
        "category": "system_metric",
        "title": "Google Cloud Run: Latencias y Concurrencia Óptimas",
        "summary": "Métricas del servicio mcp-collector en europe-west1 con escalado a 3 instancias y latencia p95 de 22ms.",
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
        "title": "Auditoría de Seguridad y Cifrado TLS 1.3",
        "summary": "Escaneo de endpoints completado: Protocolo HTTPS verificado con HSTS y certificados activos.",
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
    print(f"\n🤖 [AI Buyer Agent] Intentando comprar '{product_id}' para {persona['buyer_name']} ({persona['company']})...")

    # The lead is ingested into the system
    payload = {
        "agent_id": "autonomous-procurement-agent",
        "source_domain": f"catalog.reserve/{product_id}",
        "category": "lead",
        "title": f"🛒 Reserva Comercial: {persona['buyer_name']} ({persona['company']})",
        "summary": (
            f"El cliente {persona['buyer_name']} ({persona['buyer_email']}) de {persona['company']} "
            f"ha enviado sus datos para reservar {persona['quantity']}x '{product_id}'. Contacto guardado para seguimiento."
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
            print(f"📥 [MCP Hub] Lead capturado y publicado en tiempo real en el Dashboard!")
            print(f"💬 [Respuesta al Agente]: '⚠️ Stock agotado en el último segundo. {persona['buyer_name']} ha sido registrado en la lista de espera VIP #1.'")
        else:
            print(f"❌ Error ({res.status_code}): {res.text}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def run_simulation(base_url: str, count: int, delay: float):
    print(f"🚀 Iniciando Simulador MCP -> Destino: {base_url}")
    print(f"🎯 Modo Honeypot de Catálogo y Captura de Leads Activado\n")

    async with httpx.AsyncClient() as client:
        # 1. First simulate some buyer transactions (capturing leads)
        for i, persona in enumerate(BUYER_PERSONAS):
            await simulate_buyer_lead(client, base_url, persona)
            if delay > 0:
                await asyncio.sleep(delay)

        # 2. Simulate standard agent background telemetry
        for i in range(min(count, len(SAMPLE_INSIGHTS))):
            item = SAMPLE_INSIGHTS[i]
            url = f"{base_url}/api/insights"
            await client.post(url, json=item, timeout=10.0)
            print(f"📊 [Telemetry] Registrado insight de sistema: {item['title']}")
            if delay > 0:
                await asyncio.sleep(delay)

    print("\n🎉 Simulación completada! Abre tu dashboard en vivo para revisar los leads capturados.")


def main():
    parser = argparse.ArgumentParser(description="MCP Collector Agent & Buyer Simulator")
    parser.add_argument("--url", default="https://mcp-collector-710219361655.europe-west1.run.app", help="Base URL")
    parser.add_argument("--count", type=int, default=4, help="Number of events")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay in seconds")
    args = parser.parse_args()

    asyncio.run(run_simulation(args.url, args.count, args.delay))


if __name__ == "__main__":
    main()
