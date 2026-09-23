# -*- coding: utf-8 -*-
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from html import escape

app = FastAPI(title="Computer-Use Automation")

# Demo account state
account_balance = 12480.50
transactions = []


def page_template(content: str, title: str = "Demo Credit Union") -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | Demo Credit Union</title>

        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI",
                             Roboto, Arial, sans-serif;
                min-height: 100vh;
                background: #f4f7fb;
                color: #172b4d;
            }}

            .navbar {{
                background: #0b1f3a;
                color: white;
                padding: 18px 7%;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 3px 12px rgba(11, 31, 58, 0.15);
            }}

            .brand {{
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 21px;
                font-weight: 700;
                letter-spacing: 0.2px;
            }}

            .brand-icon {{
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: #2f80ed;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 22px;
            }}

            .secure-label {{
                font-size: 13px;
                color: #c8d6e8;
                display: flex;
                align-items: center;
                gap: 7px;
            }}

            .hero {{
                background: linear-gradient(135deg, #0b1f3a, #174a7e);
                color: white;
                padding: 42px 7% 82px;
            }}

            .hero h1 {{
                font-size: clamp(28px, 4vw, 42px);
                margin-bottom: 12px;
                font-weight: 750;
            }}

            .hero p {{
                color: #d6e5f5;
                font-size: 16px;
                max-width: 620px;
                line-height: 1.7;
            }}

            .main-container {{
                width: min(1080px, 90%);
                margin: -48px auto 50px;
                position: relative;
            }}

            .dashboard-grid {{
                display: grid;
                grid-template-columns: 1fr 1.5fr;
                gap: 24px;
            }}

            .card {{
                background: white;
                border-radius: 18px;
                padding: 30px;
                box-shadow: 0 12px 35px rgba(24, 50, 90, 0.08);
                border: 1px solid #e6edf5;
            }}

            .card h2 {{
                font-size: 21px;
                margin-bottom: 10px;
                color: #102a43;
            }}

            .card-description {{
                color: #718096;
                line-height: 1.6;
                font-size: 14px;
                margin-bottom: 25px;
            }}

            .balance-card {{
                background: linear-gradient(145deg, #1d4ed8, #2563eb);
                color: white;
                border: none;
            }}

            .balance-card h2 {{
                color: white;
            }}

            .balance-label {{
                color: #dbeafe;
                font-size: 14px;
                margin-bottom: 10px;
            }}

            .balance {{
                font-size: 36px;
                font-weight: 750;
                margin-bottom: 28px;
            }}

            .account-info {{
                border-top: 1px solid rgba(255,255,255,0.25);
                padding-top: 18px;
                display: flex;
                justify-content: space-between;
                font-size: 13px;
                color: #dbeafe;
            }}

            .form-group {{
                margin-bottom: 21px;
            }}

            label {{
                display: block;
                font-size: 14px;
                font-weight: 650;
                color: #334e68;
                margin-bottom: 8px;
            }}

            input {{
                width: 100%;
                padding: 14px 15px;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                font-size: 15px;
                color: #172b4d;
                background: #fbfdff;
                outline: none;
                transition: all 0.2s ease;
            }}

            input:focus {{
                border-color: #2563eb;
                box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
                background: white;
            }}

            .input-hint {{
                color: #829ab1;
                font-size: 12px;
                margin-top: 7px;
            }}

            .submit-button {{
                width: 100%;
                border: none;
                border-radius: 10px;
                padding: 15px;
                background: #2563eb;
                color: white;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
                transition: background 0.2s ease, transform 0.2s ease;
                margin-top: 5px;
            }}

            .submit-button:hover {{
                background: #1d4ed8;
                transform: translateY(-1px);
            }}

            .security-note {{
                display: flex;
                gap: 9px;
                align-items: flex-start;
                margin-top: 18px;
                padding: 13px;
                border-radius: 9px;
                background: #f0fdf4;
                color: #166534;
                font-size: 12px;
                line-height: 1.5;
            }}

            .success-card {{
                max-width: 650px;
                margin: 55px auto;
                text-align: center;
            }}

            .success-icon {{
                width: 72px;
                height: 72px;
                margin: 0 auto 20px;
                border-radius: 50%;
                background: #dcfce7;
                color: #15803d;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 36px;
            }}

            .success-card h1 {{
                color: #166534;
                margin-bottom: 15px;
            }}

            #success-message {{
                background: #f0fdf4;
                color: #166534;
                border: 1px solid #bbf7d0;
                border-radius: 10px;
                padding: 18px;
                line-height: 1.6;
                margin: 20px 0;
            }}

            .back-button {{
                display: inline-block;
                text-decoration: none;
                background: #2563eb;
                color: white;
                padding: 13px 24px;
                border-radius: 9px;
                font-weight: 650;
                margin-top: 10px;
            }}

            footer {{
                text-align: center;
                color: #829ab1;
                font-size: 13px;
                padding: 25px;
            }}

            @media (max-width: 760px) {{
                .dashboard-grid {{
                    grid-template-columns: 1fr;
                }}

                .navbar {{
                    padding: 15px 5%;
                }}

                .secure-label {{
                    display: none;
                }}

                .hero {{
                    padding: 32px 5% 75px;
                }}

                .main-container {{
                    width: 92%;
                }}

                .card {{
                    padding: 23px;
                }}
            }}
        
            .header-actions {{
                display: flex;
                align-items: center;
                gap: 22px;
            }}

            .logout-button {{
                color: white;
                text-decoration: none;
                border: 1px solid rgba(255,255,255,0.45);
                border-radius: 8px;
                padding: 9px 16px;
                font-size: 13px;
                font-weight: 700;
                transition: 0.2s ease;
            }}

            .logout-button:hover {{
                background: white;
                color: #0b2342;
            }}

        </style>
    </head>

    <body>
        <nav class="navbar">
            <div class="brand">
                <div class="brand-icon">DC</div>
                <span>Demo Credit Union</span>
            </div>
            <div class="header-actions">
                <div class="secure-label">Secure Banking Environment</div>
                <a href="/logout" class="logout-button">Logout</a>
            </div>
        </nav>

        {content}

        <footer>
            © 2026 Demo Credit Union · Computer-Use Automation Demo
        </footer>
    </body>
    </html>
    """



@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign In | Demo Credit Union</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background:
                    radial-gradient(circle at top left, #244f91, transparent 38%),
                    linear-gradient(135deg, #071a33, #123c6a);
                font-family: Arial, Helvetica, sans-serif;
                color: #102746;
                padding: 24px;
            }

            .login-wrapper {
                width: 100%;
                max-width: 1050px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                background: white;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 25px 70px rgba(0, 0, 0, 0.28);
            }

            .login-brand {
                background: linear-gradient(145deg, #1754d1, #2867ed);
                color: white;
                padding: 58px 48px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 610px;
            }

            .brand-header {
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 22px;
                font-weight: 700;
            }

            .brand-icon {
                width: 48px;
                height: 48px;
                border-radius: 14px;
                display: grid;
                place-items: center;
                background: rgba(255, 255, 255, 0.2);
                font-size: 21px;
                font-weight: 800;
            }

            .brand-content h1 {
                font-size: 42px;
                line-height: 1.12;
                margin-bottom: 22px;
            }

            .brand-content p {
                color: #e5efff;
                font-size: 16px;
                line-height: 1.8;
                max-width: 390px;
            }

            .brand-footer {
                color: #dbeafe;
                font-size: 13px;
                line-height: 1.7;
            }

            .login-panel {
                padding: 58px 52px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .login-panel h2 {
                font-size: 30px;
                margin-bottom: 10px;
            }

            .subtitle {
                color: #6b7b93;
                font-size: 14px;
                line-height: 1.6;
                margin-bottom: 34px;
            }

            .form-group {
                margin-bottom: 22px;
            }

            label {
                display: block;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 9px;
                color: #203b5e;
            }

            input {
                width: 100%;
                padding: 15px 16px;
                border: 1px solid #d4deeb;
                border-radius: 10px;
                outline: none;
                font-size: 14px;
                color: #173152;
                background: #fbfdff;
                transition: 0.2s ease;
            }

            input:focus {
                border-color: #2867ed;
                box-shadow: 0 0 0 4px rgba(40, 103, 237, 0.12);
                background: white;
            }

            .form-options {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 4px 0 26px;
                font-size: 13px;
            }

            .remember {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #687991;
            }

            .remember input {
                width: auto;
                accent-color: #2867ed;
            }

            .forgot {
                color: #2867ed;
                text-decoration: none;
                font-weight: 600;
            }

            .login-button {
                width: 100%;
                border: none;
                border-radius: 10px;
                padding: 16px;
                background: linear-gradient(135deg, #1754d1, #2867ed);
                color: white;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 8px 18px rgba(40, 103, 237, 0.24);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .login-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 24px rgba(40, 103, 237, 0.32);
            }

            .demo-note {
                margin-top: 24px;
                padding: 14px;
                border-radius: 10px;
                background: #effaf3;
                color: #247044;
                font-size: 12px;
                line-height: 1.6;
                text-align: center;
            }

            .security {
                text-align: center;
                color: #91a0b5;
                font-size: 12px;
                margin-top: 28px;
            }

            @media (max-width: 800px) {
                .login-wrapper {
                    grid-template-columns: 1fr;
                }

                .login-brand {
                    min-height: auto;
                    padding: 35px;
                    gap: 45px;
                }

                .brand-content h1 {
                    font-size: 32px;
                }

                .login-panel {
                    padding: 38px 30px;
                }
            }
        
            .header-actions {{
                display: flex;
                align-items: center;
                gap: 22px;
            }

            .logout-button {{
                color: white;
                text-decoration: none;
                border: 1px solid rgba(255,255,255,0.45);
                border-radius: 8px;
                padding: 9px 16px;
                font-size: 13px;
                font-weight: 700;
                transition: 0.2s ease;
            }

            .logout-button:hover {{
                background: white;
                color: #0b2342;
            }

        </style>
    </head>
    <body>
        <div class="login-wrapper">
            <section class="login-brand">
                <div class="brand-header">
                    <div class="brand-icon">DC</div>
                    <span>Demo Credit Union</span>
                </div>

                <div class="brand-content">
                    <h1>Banking made simple, secure, and personal.</h1>
                    <p>
                        Welcome to your digital banking experience.
                        Manage your money, transfer funds, and stay
                        in control of your financial journey.
                    </p>
                </div>

                <div class="brand-footer">
                    Secure demonstration environment<br>
                    Your privacy and security matter to us.
                </div>
            </section>

            <section class="login-panel">
                <h2>Welcome back</h2>
                <p class="subtitle">
                    Sign in to access your banking dashboard.
                </p>

                <form method="post" action="/login">
                    <div class="form-group">
                        <label for="username">Email Address</label>
                        <input
                            id="username"
                            name="username"
                            type="email"
                            placeholder="you@example.com"
                            required
                        >
                    </div>

                    <div class="form-group">
                        <label for="password">Password</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            placeholder="Enter your password"
                            required
                        >
                    </div>

                    <div class="form-options">
                        <label class="remember">
                            <input type="checkbox" name="remember">
                            Remember me
                        </label>

                        <a class="forgot" href="/login">
                            Forgot password?
                        </a>
                    </div>

                    <button class="login-button" type="submit">
                        Sign In to Dashboard
                    </button>
                </form>

                <div class="demo-note">
                    Demo credentials:<br>
                    <strong>demo@creditunion.test</strong> /
                    <strong>demo123</strong>
                </div>

                <div class="security">
                    Protected demo environment ? No real banking data
                </div>
            </section>
        </div>
    </body>
    </html>
    """


@app.post("/login", response_class=HTMLResponse)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    if username == "demo@creditunion.test" and password == "demo123":
        return RedirectResponse(url="/dashboard", status_code=303)

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login Failed | Demo Credit Union</title>
        <meta http-equiv="refresh" content="2;url=/login">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f3f6fb;
                display: grid;
                place-items: center;
                min-height: 100vh;
                color: #173152;
            }}
            .message {
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 12px 35px rgba(0,0,0,.1);
                text-align: center;
            }}
            h2 { color: #c0392b; margin-bottom: 12px; }
        
            .header-actions {{
                display: flex;
                align-items: center;
                gap: 22px;
            }}

            .logout-button {{
                color: white;
                text-decoration: none;
                border: 1px solid rgba(255,255,255,0.45);
                border-radius: 8px;
                padding: 9px 16px;
                font-size: 13px;
                font-weight: 700;
                transition: 0.2s ease;
            }}

            .logout-button:hover {{
                background: white;
                color: #0b2342;
            }}

        </style>
    </head>
    <body>
        <div class="message">
            <h2>Sign-in unsuccessful</h2>
            <p>Invalid email or password. Returning to login...</p>
        </div>
    </body>
    </html>
    """



@app.get("/logout")
def logout():
    return RedirectResponse(url="/login", status_code=303)


@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
def home():
    global account_balance, transactions

    if transactions:
        transactions_html = "".join(
            f"""
            <div style="display:flex;justify-content:space-between;
                        align-items:center;padding:12px 0;
                        border-bottom:1px solid rgba(255,255,255,0.18);
                        font-size:13px;">
                <div>
                    <div style="font-weight:650;">Transfer to {escape(item["account"])}</div>
                    <div style="color:#dbeafe;margin-top:4px;">{item["date"]}</div>
                </div>
                <strong style="color:#fecaca;">-${item["amount"]:,.2f}</strong>
            </div>
            """
            for item in transactions[-4:][::-1]
        )
    else:
        transactions_html = """
        <p style="color:#dbeafe;font-size:13px;margin-top:18px;">
            No recent transactions
        </p>
        """

    content = f"""
    <section class="hero">
        <h1>Good morning, welcome back.</h1>
        <p>
            Manage your finances securely and transfer funds with confidence
            through your digital banking dashboard.
        </p>
    </section>

    <main class="main-container">
        <div class="dashboard-grid">
            <section class="card balance-card">
                <h2>Account Overview</h2>
                <p class="balance-label">Available Balance</p>
                <div class="balance">${account_balance:,.2f}</div>

                <div class="account-info">
                    <span>Checking Account</span>
                    <span>XXXX 4821</span>
                </div>

                <div style="margin-top:30px;">
                    <h3 style="font-size:15px;margin-bottom:8px;">
                        Recent Transactions
                    </h3>
                    {transactions_html}
                </div>
            </section>

            <section class="card">
                <h2>Transfer Funds</h2>
                <p class="card-description">
                    Send money to another account quickly and securely.
                    Please verify the details before submitting.
                </p>

                <form method="post" action="/transfer">
                    <div class="form-group">
                        <label for="account_number">Recipient Account Number</label>
                        <input
                            id="account_number"
                            name="account_number"
                            type="text"
                            inputmode="numeric"
                            pattern="[0-9]{{9}}"
                            minlength="9"
                            maxlength="9"
                            placeholder="Enter recipient account number"
                            required
                        />
                        <p class="input-hint">
                            Enter the 9-digit recipient account number.
                        </p>
                    </div>

                    <div class="form-group">
                        <label for="amount">Transfer Amount (USD)</label>
                        <input
                            id="amount"
                            name="amount"
                            type="number"
                            step="0.01"
                            min="0.01"
                            max="{account_balance:.2f}"
                            placeholder="0.00"
                            required
                        />
                    </div>

                    <button class="submit-button" type="submit">
                        Review and Submit Transfer
                    </button>

                    <div class="security-note">
                        <span>SECURE</span>
                        <span>
                            Your transfer is processed in a secure demonstration
                            environment. Never share your banking credentials.
                        </span>
                    </div>
                </form>
            </section>
        </div>
    </main>
    """

    return page_template(content)


@app.post("/transfer", response_class=HTMLResponse)
def transfer(account_number: str = Form(...), amount: float = Form(...)):
    global account_balance, transactions

    account_number = account_number.strip()

    if amount <= 0:
        message = "Please enter a transfer amount greater than zero."
        title = "Transfer Error"
        icon = "!"
    elif amount > account_balance:
        message = (
            f"Insufficient funds. Your available balance is "
            f"${account_balance:,.2f}."
        )
        title = "Transfer Declined"
        icon = "!"
    else:
        account_balance -= amount

        from datetime import datetime

        transactions.append({
            "account": account_number,
            "amount": amount,
            "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
        })

        message = (
            f"Transfer of ${amount:.2f} to account {escape(account_number)} "
            "was submitted successfully."
        )
        title = "Transfer Confirmation"
        icon = "OK"

    content = f"""
    <main class="main-container">
        <section class="card success-card">
            <div class="success-icon">{icon}</div>
            <h1>{title}</h1>

            <p id="success-message">
                {message}
            </p>

            <p class="card-description">
                Your transfer request has been recorded in this demonstration.
                No real funds were moved.
            </p>

            <a class="back-button" href="/">
                Back to Dashboard
            </a>
        </section>
    </main>
    """

    return page_template(content, title)


@app.get("/health")
def health():
    return {"status": "healthy"}