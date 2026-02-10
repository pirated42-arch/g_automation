#!/usr/bin/env python3
"""
🤖 1-YEAR HUMAN ACTIVITY BOOSTER
3 commits/week + 6-8 every 3 weeks = PERFECTLY NATURAL
"""

# ... (keep all your existing imports) ...

class AutonomousGitHubBooster:
    # ... (keep existing __init__ and other methods) ...
    
    async def generate_realistic_schedule(self):
        """1-YEAR HUMAN PATTERN: 3/wk + bonus every 3 weeks"""
        schedule = []
        
        # Weekly pattern (always 3+ commits)
        weekly = await self.generate_weekly_schedule()
        schedule.extend(weekly)
        
        # Check for bonus week (every ~21 days)
        today = pendulum.now(self.tz).day
        if today % 21 in [0, 1, 2]:  # 3-day window every 3 weeks
            bonus = await self.generate_bonus_day()
            schedule.extend(bonus)
        
        # Save to DB
        for entry in schedule:
            await self.db.execute(
                "INSERT OR IGNORE INTO schedule (timestamp, repo_url, type) VALUES (?, ?, ?)",
                (entry['timestamp'], entry['repo_url'], entry['type'])
            )
        
        await self.db.commit()
        logger.info(f"📅 Generated {len(schedule)} commits (human pattern)")
        return schedule
    
    async def generate_weekly_schedule(self):
        """3 commits/week + natural weekend variance"""
        schedule = []
        weekdays = [0,1,2,3,4]  # Mon-Fri
        
        # ALWAYS 3 weekday commits (different days)
        active_days = random.sample(weekdays, 3)
        for day_offset in active_days:
            date = pendulum.now(self.tz).add(days=day_offset)
            schedule.append(self._make_commit(date, 'regular'))
        
        # 40% weekend (looks like real dev)
        if random.random() < 0.4:
            weekend = random.choice([5,6])
            date = pendulum.now(self.tz).add(days=weekend)
            schedule.append(self._make_commit(date, 'weekend'))
        
        return schedule
    
    async def generate_bonus_day(self):
        """6-8 commits on release/update day"""
        bonus_count = random.randint(6, 8)
        date = pendulum.now(self.tz)
        return [self._make_commit(date, 'bonus') for _ in range(bonus_count)]
    
    def _make_commit(self, date, commit_type):
        """Ultra-realistic timing"""
        patterns = {
            'regular': [(8,19), 120],    # 8AM-7PM, ±2hr gaps
            'weekend': [(10,16), 90],    # 10AM-4PM weekends
            'bonus': [(9,17), 45]        # Workday 9-5, tight gaps
        }
        
        hour_range, jitter = patterns[commit_type]
        hour = random.randint(*hour_range)
        minute = random.choice([8,15,22,27,34,42,46,58])  # HUMAN MINUTES!
        
        commit_time = date.hour(hour).minute(minute)
        repo = random.choice(self.config['repos'])
        
        return {
            'timestamp': commit_time.to_iso8601_string(),
            'repo_url': repo,
            'type': commit_type
        }

# Update main loop
async def run_forever(self):
    while self.running:
        await self.generate_realistic_schedule()
        
        # Process ALL pending commits
        async with self.db.execute("SELECT id FROM schedule WHERE status='pending' ORDER BY timestamp") as cursor:
            commits = await cursor.fetchall()
            
        for (commit_id,) in commits[:3]:  # Max 3/hr
            await self.process_commit(commit_id)
            await asyncio.sleep(random.randint(7200, 10800))  # 2-3hr gaps
        
        await asyncio.sleep(3600)  # 1hr heartbeat