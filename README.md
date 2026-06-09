# Competitive Intelligence Agent

An autonomous AI agent that monitors competitors on a schedule, aggregates what it finds, and delivers a structured intelligence report. It replaces the manual work of checking competitor sites and review platforms by hand.

## What it does

The agent scrapes competitor websites and G2 review data, uses an LLM to summarize and structure the findings, and writes a clean intelligence report to a Google Sheet. It runs on a schedule with no manual trigger, so the report stays current on its own.

## How it works

1. Scrapes target competitor websites and their G2 review pages
2. Parses the raw content into usable text
3. Sends the content to an LLM to extract and structure the key signals
4. Writes a formatted intelligence report to a Google Sheet
5. Runs automatically on a recurring schedule

## Tech stack

- Python
- OpenAI API for summarizing and structuring findings
- Beautiful Soup for web scraping
- Google Sheets API for report delivery
- GitHub Actions for scheduled, serverless execution

## Why it matters

Competitive monitoring is usually a recurring manual chore that slips when people get busy. This agent does it consistently and on its own, so go-to-market teams get a reliable, up-to-date read on the landscape without anyone having to remember to check.
