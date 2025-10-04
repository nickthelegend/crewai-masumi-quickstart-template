#!/usr/bin/env python3
"""
Direct test of ResumeCrew using crew_definition.py
"""

def test_crew_direct():
    """Test ResumeCrew directly"""
    
    resume_data = {
        "text": """
        Name: Alex Chen
        Email: alex.chen@email.com
        Phone: (555) 234-5678
        Location: Seattle, WA
        
        Professional Summary:
        Senior DevOps Engineer with 6+ years of experience in cloud infrastructure and automation.
        
        Work Experience:
        - Senior DevOps Engineer at CloudTech (2021-2024)
          * Managed AWS infrastructure for 100+ microservices
          * Reduced deployment time by 75% with automated CI/CD
          * Led migration to Kubernetes saving $200K annually
        
        - DevOps Engineer at StartupCorp (2018-2021)
          * Built infrastructure automation using Terraform
          * Implemented monitoring and alerting systems
          * Maintained 99.9% uptime for production systems
        
        Education:
        - Bachelor of Science in Computer Engineering
          University of Washington (2014-2018)
        
        Skills:
        AWS, Docker, Kubernetes, Terraform, Jenkins, Python, Bash, Monitoring
        """
    }
    
    print("Testing ResumeCrew with real MCP integration...")
    
    try:
        from crew_definition import ResumeCrew
        
        print("Initializing ResumeCrew...")
        crew = ResumeCrew(verbose=True)
        
        print("Running crew with resume data...")
        result = crew.crew.kickoff(resume_data)
        
        print("Crew execution completed!")
        print(f"Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_crew_direct()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")