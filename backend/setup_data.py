#!/usr/bin/env python
"""
Automated setup script for creating initial users and tasks.
Run this after migrations to populate database with test data.

Usage:
    docker-compose exec backend python setup_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()

def create_users():
    """Create admin and regular users if they don't exist."""
    print("\n" + "="*60)
    print("Creating Users...")
    print("="*60)
    
    # Create admin
    if not User.objects.filter(email='admin@test.com').exists():
        admin = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Admin created: {admin.email}")
    else:
        print("⚠️  Admin already exists: admin@test.com")
    
    # Create user1
    if not User.objects.filter(email='user1@test.com').exists():
        user1 = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            password='user123'
        )
        print(f"✅ User created: {user1.email}")
    else:
        print("⚠️  User already exists: user1@test.com")
    
    # Create user2
    if not User.objects.filter(email='user2@test.com').exists():
        user2 = User.objects.create_user(
            email='user2@test.com',
            username='user2',
            password='user123'
        )
        print(f"✅ User created: {user2.email}")
    else:
        print("⚠️  User already exists: user2@test.com")

def create_tasks():
    """Create sample tasks for users."""
    print("\n" + "="*60)
    print("Creating Sample Tasks...")
    print("="*60)
    
    try:
        user1 = User.objects.get(email='user1@test.com')
        user2 = User.objects.get(email='user2@test.com')
    except User.DoesNotExist:
        print("❌ Users not found. Create users first!")
        return
    
    # Tasks for user1
    tasks_user1 = [
        {'title': 'Complete Django Backend', 'description': 'Finish the admin panel implementation', 'status': 'TODO'},
        {'title': 'Review Pull Requests', 'description': 'Check and merge pending PRs', 'status': 'DOING'},
        {'title': 'Setup CI/CD Pipeline', 'description': 'Configure GitHub Actions', 'status': 'DONE'},
    ]
    
    for task_data in tasks_user1:
        if not Task.objects.filter(title=task_data['title'], author=user1).exists():
            Task.objects.create(author=user1, **task_data)
            print(f"✅ Task created for user1: {task_data['title']}")
        else:
            print(f"⚠️  Task already exists: {task_data['title']}")
    
    # Tasks for user2
    tasks_user2 = [
        {'title': 'Write API Documentation', 'description': 'Document all REST endpoints', 'status': 'TODO'},
        {'title': 'Fix Reported Bugs', 'description': 'Address issues from testing', 'status': 'DOING'},
    ]
    
    for task_data in tasks_user2:
        if not Task.objects.filter(title=task_data['title'], author=user2).exists():
            Task.objects.create(author=user2, **task_data)
            print(f"✅ Task created for user2: {task_data['title']}")
        else:
            print(f"⚠️  Task already exists: {task_data['title']}")

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("🚀 STARTING AUTOMATED DATA SETUP")
    print("="*60)
    
    create_users()
    create_tasks()
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\nYou can now login with:")
    print("\n👑 Admin:")
    print("   Email: admin@test.com")
    print("   Password: admin123")
    print("\n👤 Regular Users:")
    print("   Email: user1@test.com | Password: user123")
    print("   Email: user2@test.com | Password: user123")
    print("\n🌐 Access the app at: http://localhost:5173")
    print("👑 Admin panel at: http://localhost:5173/admin")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
