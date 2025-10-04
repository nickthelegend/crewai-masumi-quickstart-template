#!/usr/bin/env python3
"""
Test file for ResumeCrew - generates a sample resume and converts it to PDF
"""

from crew_definition import ResumeCrew

def test_resume_generation():
    """Test the resume generation and PDF conversion workflow"""
    
    # Sample resume data
    resume_data = {
        "text": """
        Name: John Smith
        Email: john.smith@email.com
        Phone: (555) 123-4567
        Location: New York, NY
        
        Professional Summary:
        Experienced software engineer with 5+ years developing web applications using Python, JavaScript, and React.
        
        Work Experience:
        - Senior Software Engineer at TechCorp (2021-2024)
          * Led development of microservices architecture
          * Improved system performance by 40%
          * Mentored junior developers
        
        - Software Engineer at StartupXYZ (2019-2021)
          * Built full-stack web applications
          * Implemented CI/CD pipelines
          * Collaborated with cross-functional teams
        
        Education:
        - Bachelor of Science in Computer Science
          University of Technology (2015-2019)
        
        Skills:
        Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL, Git
        """
    }
    
    print("🚀 Starting ResumeCrew test...")
    
    try:
        # Initialize the crew
        crew = ResumeCrew(verbose=True)
        print("✅ ResumeCrew initialized successfully")
        
        # Run the crew with sample data
        print("🔄 Running resume generation and PDF conversion...")
        result = crew.crew.kickoff(resume_data)
        
        print("✅ Crew execution completed!")
        print(f"📄 Result: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        raise

if __name__ == "__main__":
    test_resume_generation()