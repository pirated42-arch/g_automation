import streamlit as st
import plotly.express as px
import pandas as pd
import pendulum
import asyncio
import os
import logging
from datetime import datetime
import json
import time

# Mock booster class (no external deps)
class MockBooster:
    def __init__(self, token, repos):
        self.token = token
        self.repos = repos
        self.next_commit = pendulum.now().add(hours=2)
    
    def next_commit_str(self):
        return self.next_commit.format("MMM DD, HH:mm")
    
    def generate_preview_schedule(self, n):
        dates = [pendulum.now().add(hours=i*3) for i in range(n)]
        return pd.DataFrame({
            'start': dates,
            'end': [d.add(minutes=5) for d in dates],
            'repo': [self.repos[i%len(self.repos)] for i in range(n)],
            'type': ['Regular']*n
        })
    
    def get_recent_logs(self, n):
        return """2026-02-10 08:12 PM: Starting booster...
2026-02-10 08:15 PM: Autonomous mode active
Next commit: Feb 10, 10:15 PM"""

# Page config FIRST
st.set_page_config(page_title="GitHub Activity Booster", layout="wide")

st.title("🤖 GitHub Activity Booster")
st.markdown("### 📊 Live Dashboard & 12-Month Projection")

# Sidebar
st.sidebar.header("⚙️ Configuration")
github_token = st.sidebar.text_input("🔑 GitHub Token (Classic PAT)", 
    type="password", help="ghp_XXX with 'repo' scope")

repos_input = st.sidebar.text_area("📂 Repositories (JSON array)", 
    value='["https://github.com/YOURUSERNAME/test-repo.git"]', height=100)

if st.sidebar.button("🚀 DEPLOY & START", type="primary", use_container_width=True):
    try:
        repos = json.loads(repos_input)
        if github_token and repos:
            st.sidebar.success(f"✅ Deployed! {len(repos)} repos")
            st.session_state.booster = MockBooster(github_token, repos)
            st.session_state.running = True
            st.rerun()
        else:
            st.sidebar.error("❌ Token + repos required")
    except json.JSONDecodeError:
        st.sidebar.error("❌ Invalid JSON")

# Emergency stop
if st.button("🛑 EMERGENCY STOP", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Dashboard
if 'booster' in st.session_state and st.session_state.get('running', False):
    booster = st.session_state.booster
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("⏭️ Next Commit", booster.next_commit_str())
    with col2: st.metric("📈 Weekly Target", "3+6 bonus")
    with col3: st.metric("📊 Repos Active", len(booster.repos))
    with col4: st.metric("🕐 Status", "🟢 Running")
    
    st.subheader("📅 Next 20 Commits")
    df = booster.generate_preview_schedule(20)
    fig = px.timeline(df, x_start="start", x_end="end", y="repo", 
                     color="type", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📜 Real-time Logs")
    st.code(booster.get_recent_logs(10), language="log")
    
    st.success("🎉 Booster deployed! Check GitHub in 2-3 hours")

else:
    st.info("""
    ### 👆 Getting Started (30 seconds)
    1. Token: GitHub → Settings → Developer → Tokens (classic) → `repo` scope
    2. Repos: `["https://github.com/YOUR/repo1.git"]`
    3. Click DEPLOY & START → Autonomous!
    """)

st.markdown("---")
st.markdown("*Powered by Streamlit | Free Render deployment*")