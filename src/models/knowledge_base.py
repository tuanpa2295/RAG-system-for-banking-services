"""
Banking Knowledge Base

Comprehensive collection of banking and financial services documents.
This module contains all the domain knowledge used by the RAG system.
"""

from typing import List
from .banking_models import BankingDocument

def get_banking_knowledge_base() -> List[BankingDocument]:
    """
    Create a comprehensive banking knowledge base.
    
    Returns:
        List[BankingDocument]: List of banking documents covering all major
                              banking services and policies
    """
    return [
        BankingDocument(
            id="doc_001",
            title="Personal Loan Requirements",
            content="""Personal loan requirements include: minimum age of 21 years, maximum age of 65 years at loan maturity, minimum monthly income of $3,000, employment history of at least 2 years, good credit score (minimum 650), debt-to-income ratio below 40%, valid identification documents, proof of income (pay stubs, tax returns), and bank statements for the last 6 months. Loan amounts range from $1,000 to $100,000 with terms from 12 to 84 months. Interest rates vary based on creditworthiness, typically ranging from 5.99% to 24.99% APR.""",
            category="loans",
            source="lending_policies.pdf"
        ),
        BankingDocument(
            id="doc_002", 
            title="Savings Account Features and Benefits",
            content="""Our savings accounts offer competitive interest rates, no monthly maintenance fees with minimum balance of $100, online and mobile banking access, ATM network access at 60,000+ locations nationwide, FDIC insurance up to $250,000 per depositor, automatic savings programs, direct deposit capabilities, and 24/7 customer service. Premium savings accounts require $10,000 minimum balance and offer higher interest rates, relationship banking benefits, and waived fees on other services.""",
            category="accounts",
            source="product_guide.pdf"
        ),
        BankingDocument(
            id="doc_003",
            title="Credit Card Application Process",
            content="""Credit card application process: complete online application with personal information, employment details, and financial information. Required documents include valid government-issued ID, Social Security number, proof of income, and employment verification. Processing time is typically 7-10 business days. Approval factors include credit score (minimum 600 for basic cards, 700+ for premium cards), income verification, debt-to-income ratio, and credit history length. New cardholders receive welcome bonuses, 0% introductory APR for 12 months, and fraud protection.""",
            category="credit",
            source="credit_policies.pdf"
        ),
        BankingDocument(
            id="doc_004",
            title="Investment Account Options",
            content="""Investment account options include Individual Retirement Accounts (IRA), Roth IRA, 401(k) rollovers, brokerage accounts, mutual funds, ETFs, and certificate of deposits. Minimum opening deposits vary: $500 for IRAs, $1,000 for brokerage accounts, $100 for CDs. Investment advisory services available with certified financial planners. Risk assessment and portfolio recommendations based on age, income, and retirement goals. Online trading platform with research tools, market analysis, and educational resources.""",
            category="investments",
            source="investment_guide.pdf"
        ),
        BankingDocument(
            id="doc_005",
            title="Mobile Banking Security Features",
            content="""Mobile banking security includes multi-factor authentication, biometric login (fingerprint, face ID), 256-bit SSL encryption, real-time fraud monitoring, transaction alerts, device registration, session timeout, and secure messaging. Additional features: mobile check deposit, bill pay, account transfers, ATM locator, spending categorization, and budget tracking. Security tips: use strong passwords, enable automatic app updates, avoid public Wi-Fi for banking, and report suspicious activity immediately.""",
            category="security",
            source="security_manual.pdf"
        ),
        BankingDocument(
            id="doc_006",
            title="Mortgage Loan Process and Requirements",
            content="""Mortgage loan process: pre-qualification, application submission, documentation review, property appraisal, underwriting, and closing. Required documents include income verification (W-2s, pay stubs, tax returns), bank statements, credit reports, employment verification, and property documentation. Down payment requirements: conventional loans 5-20%, FHA loans 3.5%, VA loans 0%. Loan terms: 15, 20, or 30 years. Interest rates based on credit score, down payment, and market conditions. Closing costs typically 2-5% of loan amount.""",
            category="loans",
            source="mortgage_guidelines.pdf"
        ),
        BankingDocument(
            id="doc_007",
            title="Business Banking Services",
            content="""Business banking services include business checking accounts, savings accounts, credit lines, merchant services, payroll processing, and cash management solutions. Account requirements: business license, EIN number, articles of incorporation, and business plan. Features: online banking, mobile deposits, wire transfers, ACH processing, and dedicated relationship managers. Loan products: equipment financing, working capital loans, SBA loans, and commercial real estate financing. Treasury management services for larger businesses.""",
            category="business",
            source="business_services.pdf"
        ),
        BankingDocument(
            id="doc_008",
            title="Federal Banking Regulations and Compliance",
            content="""Key federal banking regulations include FDIC insurance requirements, Truth in Lending Act (TILA), Fair Credit Reporting Act (FCRA), Equal Credit Opportunity Act (ECOA), Bank Secrecy Act (BSA), and Anti-Money Laundering (AML) requirements. Customer identification programs (CIP) required for new accounts. Privacy notices under Gramm-Leach-Bliley Act. Regulation E covers electronic fund transfers. Regulation Z implements TILA for credit disclosures. Compliance monitoring and reporting requirements for suspicious activities.""",
            category="regulations",
            source="compliance_manual.pdf"
        ),
        BankingDocument(
            id="doc_009",
            title="Interest Rates and Fee Structure",
            content="""Current interest rates: savings accounts 0.50%-2.50% APY, money market accounts 1.00%-3.00% APY, CDs 1.50%-4.50% APY based on term length. Loan rates: personal loans 5.99%-24.99% APR, auto loans 3.49%-15.99% APR, mortgages 6.25%-8.75% APR. Fee structure: overdraft fees $35, ATM fees $3 (out-of-network), wire transfer fees $25 domestic/$50 international, stop payment fees $30, account closure fees $25 (within 90 days).""",
            category="rates",
            source="rate_sheet.pdf"
        ),
        BankingDocument(
            id="doc_010",
            title="Customer Service and Support Channels",
            content="""Customer service available through multiple channels: 24/7 phone support, online chat, email support, branch locations, and mobile app messaging. Specialized support teams for different services: mortgage specialists, investment advisors, business banking experts, and fraud prevention team. Self-service options: online banking, mobile app, ATM network, and FAQ resources. Response times: phone calls answered within 2 minutes, chat within 1 minute, emails within 24 hours. Customer satisfaction ratings and feedback programs.""",
            category="support",
            source="service_standards.pdf"
        ),
        BankingDocument(
            id="doc_011",
            title="Cryptocurrency and Digital Asset Services",
            content="""Our bank now offers cryptocurrency services including Bitcoin and Ethereum trading, digital wallet management, and blockchain-based transactions. Services include: cryptocurrency buying/selling with competitive rates, secure digital wallet storage, integration with traditional banking accounts, regulatory compliance with federal guidelines, and educational resources about digital assets. Minimum investment is $100, with transaction fees of 1.5%. Available through our mobile app and online banking platform. All cryptocurrency transactions are FDIC-insured up to regulatory limits.""",
            category="digital",
            source="crypto_services.pdf"
        ),
        BankingDocument(
            id="personal_loan_guide",
            title="Personal Loan Requirements and Application Process",
            content="""Personal Loan Requirements: Minimum age 21 years, minimum credit score 650, annual income of $30,000+, debt-to-income ratio below 40%, US citizenship or permanent residency required. Employment verification needed with 2+ years stable employment history. Required documents include: government-issued ID, Social Security card, proof of income (pay stubs, tax returns), bank statements from last 3 months, employment verification letter. Loan amounts range from $5,000 to $50,000 with terms of 2-7 years. Interest rates from 6.99% to 24.99% APR based on creditworthiness. No collateral required. Application can be completed online, by phone, or in-branch. Processing time 1-3 business days for approval, funding within 24 hours of approval. No prepayment penalties. Late payment fee $25. Origination fee 1-5% of loan amount depending on credit profile.""",
            category="loans",
            source="personal_loan_guide.pdf"
        ),
        BankingDocument(
            id="doc_012",
            title="Comprehensive Financial Planning Services",
            content="""Financial planning services include retirement planning, college savings plans (529 plans), estate planning, tax optimization strategies, and wealth management. Our certified financial planners provide personalized consultations, portfolio analysis, risk assessment, and long-term financial goal setting. Services available for accounts with $50,000+ balance. Planning fees: $200 initial consultation, $150/hour ongoing advisory. Includes annual portfolio review, tax planning strategies, insurance analysis, and beneficiary planning.""",
            category="planning",
            source="financial_planning.pdf"
        ),
        BankingDocument(
            id="doc_013",
            title="Small Business Loan Programs",
            content="""Small business loan programs include SBA 7(a) loans up to $5 million, SBA microloans up to $50,000, equipment financing, commercial real estate loans, and business lines of credit. Requirements: business plan, financial statements, personal guarantee, collateral (varies by loan type), good credit score (680+), and business operating for 2+ years. Interest rates range from 5.5% to 12% based on loan type and creditworthiness. Application process includes business evaluation, financial analysis, and approval timeline of 30-45 days.""",
            category="business",
            source="sba_loan_guide.pdf"
        ),
        BankingDocument(
            id="doc_014",
            title="Wealth Management and Private Banking",
            content="""Private banking services for high-net-worth clients with $1 million+ in assets. Services include dedicated relationship managers, customized investment portfolios, estate planning, tax strategies, trust services, and exclusive banking benefits. Investment options: alternative investments, hedge funds, private equity, real estate investment trusts (REITs), and international markets. Additional perks: priority customer service, waived fees, exclusive events, and concierge services. Minimum account balance requirements and fee structures vary by service level.""",
            category="wealth",
            source="private_banking_guide.pdf"
        ),
        BankingDocument(
            id="doc_015",
            title="Online and Mobile Banking Features",
            content="""Digital banking platform features: account management, bill pay, money transfers, mobile check deposit, budgeting tools, spending alerts, and financial insights. Advanced features: scheduled payments, recurring transfers, account aggregation, goal tracking, and expense categorization. Security features: two-factor authentication, biometric login, transaction monitoring, and fraud alerts. Customer support through chat, video calls, and screen sharing. Available 24/7 with offline capabilities for account viewing.""",
            category="digital",
            source="digital_banking_guide.pdf"
        ),
        BankingDocument(
            id="doc_016",
            title="Auto Loan Financing Options",
            content="""Auto loan financing available for new and used vehicles. New car loans: rates from 3.99% to 8.99% APR, terms up to 84 months, up to 100% financing available. Used car loans: rates from 4.99% to 12.99% APR, terms up to 72 months, vehicles up to 7 years old eligible. Required documents: proof of income, insurance coverage, vehicle information, and driver's license. Pre-approval available online. Loan amounts from $5,000 to $100,000. No prepayment penalties. Gap insurance and extended warranty options available.""",
            category="loans",
            source="auto_loan_guide.pdf"
        ),
        BankingDocument(
            id="doc_017",
            title="Home Equity Line of Credit (HELOC)",
            content="""Home Equity Line of Credit provides flexible access to your home's equity. Credit limits up to 80% of home value minus existing mortgage balance. Variable interest rates starting at Prime + 0.5%. Draw period: 10 years with interest-only payments. Repayment period: 15 years with principal and interest payments. No closing costs on lines up to $250,000. Uses include home improvements, debt consolidation, education expenses, and major purchases. Required: home appraisal, income verification, and good credit score (720+).""",
            category="loans",
            source="heloc_guide.pdf"
        ),
        BankingDocument(
            id="doc_018",
            title="Student Loan Services and Refinancing",
            content="""Student loan services include federal loan servicing, private student loans, and refinancing options. Private loans: competitive rates, flexible repayment terms, no origination fees, and cosigner release options. Refinancing benefits: potentially lower rates, simplified payments, and flexible terms. Eligibility: good credit score, stable income, and graduation from eligible institution. Student checking accounts with no monthly fees, overdraft protection, and financial literacy resources. Parent PLUS loan alternatives available.""",
            category="loans",
            source="student_loan_services.pdf"
        ),
        BankingDocument(
            id="doc_019",
            title="Foreign Exchange and International Banking",
            content="""International banking services include foreign exchange, wire transfers, international trade finance, and multi-currency accounts. Foreign exchange: competitive rates for 50+ currencies, online rate calculator, and currency delivery services. International wire transfers: same-day processing, competitive fees, and real-time tracking. Services for expatriates: international account access, global ATM network, and cross-border investment options. Trade finance: letters of credit, documentary collections, and export financing.""",
            category="international",
            source="international_services.pdf"
        ),
        BankingDocument(
            id="doc_020",
            title="Insurance Products and Protection Services",
            content="""Insurance products available through banking partnerships: life insurance, disability insurance, home insurance, auto insurance, and identity theft protection. Life insurance options: term life, whole life, and universal life policies. Disability insurance: short-term and long-term coverage for income protection. Identity theft protection includes credit monitoring, fraud alerts, and resolution services. Insurance premium financing available. Bundled packages offer discounts when combined with banking services.""",
            category="insurance",
            source="insurance_products.pdf"
        ),
        BankingDocument(
            id="doc_021",
            title="ATM and Branch Network Services",
            content="""Extensive ATM network with 75,000+ locations nationwide and international access. Branch services: personal banker consultations, safe deposit boxes, notary services, and cashier's checks. ATM services: cash withdrawal, deposits, balance inquiries, mini-statements, and cardless access via mobile app. International ATM access in 200+ countries. ATM fees: free at network locations, $3 fee for out-of-network usage with reimbursement programs for premium accounts. Extended branch hours and weekend availability at select locations.""",
            category="services",
            source="branch_atm_guide.pdf"
        ),
        BankingDocument(
            id="doc_022",
            title="Credit Building and Repair Services",
            content="""Credit building services include secured credit cards, credit monitoring, and financial education programs. Secured credit card: $200-$5,000 credit limit based on deposit, graduates to unsecured card after 12 months of good payment history. Credit monitoring: free credit scores, alerts for changes, and identity monitoring. Credit repair consultations available with certified counselors. Financial literacy workshops covering budgeting, credit management, and debt reduction strategies. Young adult programs for building first-time credit.""",
            category="credit",
            source="credit_building_guide.pdf"
        ),
        BankingDocument(
            id="doc_023",
            title="Senior Banking Services and Benefits",
            content="""Senior banking services for customers 65+: free checking accounts, enhanced fraud protection, large-font statements, and dedicated customer service. Additional benefits: waived fees on cashier's checks, money orders, and safe deposit boxes. Investment services: conservative portfolio options, income-focused strategies, and estate planning assistance. Health Savings Account (HSA) management for medical expenses. Senior discounts on loan rates and insurance products. Educational seminars on retirement planning and Medicare supplements.""",
            category="senior",
            source="senior_services_guide.pdf"
        ),
        BankingDocument(
            id="doc_024",
            title="Environmental and Sustainable Banking",
            content="""Sustainable banking initiatives include paperless statements, carbon-neutral operations, and green financing options. Green loans: energy-efficient home improvements, solar panel financing, and electric vehicle loans with reduced rates. Environmental impact: renewable energy investments, sustainable business lending, and carbon offset programs. Electronic services: mobile banking, online bill pay, and digital documents to reduce paper usage. Community investments in renewable energy projects and environmental conservation programs.""",
            category="sustainability",
            source="green_banking_guide.pdf"
        ),
        BankingDocument(
            id="doc_025",
            title="Youth and Student Banking Programs",
            content="""Youth banking programs for ages 13-24: free checking and savings accounts, financial literacy education, and scholarship opportunities. Student accounts: no monthly fees, free ATM access, overdraft forgiveness, and budgeting tools. Youth savings accounts with competitive rates and goal-setting features. Parent-child joint accounts with spending controls and monitoring. Educational resources: online financial courses, budgeting apps, and money management workshops. College banking packages with special rates and services.""",
            category="youth",
            source="youth_banking_guide.pdf"
        )
    ]
