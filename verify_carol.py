import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Splash Screen
        await page.goto(f'http://localhost:8000/carol_platform.html')
        await page.wait_for_selector('.splash-logo:has-text("CAROL")')
        await page.screenshot(path='platform_splash.png')
        print("Captured platform_splash.png")

        # 2. Registration Form
        print("Clicking Registrarse e Iniciar...")
        await page.click('button:has-text("Registrarse e Iniciar")')
        await page.wait_for_selector('h2:has-text("Registro de Participante")', state='visible')
        await page.screenshot(path='platform_registration.png')
        print("Captured platform_registration.png")

        # 3. Fill registration and check Level Routing (e.g., Medium)
        print("Filling registration form...")
        await page.fill('#reg-name', 'Juan Garcia')
        await page.fill('#reg-id', 'EMP-1234')
        await page.fill('#reg-company', 'Test Company')
        await page.fill('#reg-email', 'test@example.com')
        await page.select_option('#reg-dept', 'production')
        await page.select_option('#reg-role', 'process_tech')
        await page.select_option('#reg-birth-year', '1990')
        await page.fill('#reg-exp', '4')
        # self-eval is a range, 60% should trigger Medium
        await page.evaluate('document.getElementById("reg-self-eval").value = 60')

        print("Submitting registration...")
        await page.click('button:has-text("Continuar a Instrucciones")')

        # 4. Instructions (Level should be Medium)
        print("Waiting for Instructions — Medio...")
        await page.wait_for_selector('#inst-title:has-text("Instrucciones — Medio")', state='visible')
        await page.screenshot(path='platform_instructions.png')
        print("Captured platform_instructions.png")

        # 5. Admin Dashboard
        print("Opening Admin Dashboard...")
        await page.goto(f'http://localhost:8000/admin.html')
        await page.wait_for_selector('h2:has-text("CAROL Admin")', state='visible')
        await page.screenshot(path='admin_dashboard.png')
        print("Captured admin_dashboard.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
