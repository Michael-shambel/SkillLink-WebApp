import requests

BASE_URL = "http://localhost:8000/api/"
JOBSEEKER_TOKEN = None
EMPLOYER_TOKEN = None


def register_user():
    print("Create An Account")
    email = input("Enter email: ")
    password = input("Enter password: ")
    is_employer = input("Is this an employer account? (y/n): ").lower() == 'y'
    is_jobseeker = not is_employer

    data = {
        "email": email,
        "password": password,
        "is_employer": is_employer,
        "is_jobseeker": is_jobseeker
    }

    try:
        response = requests.post(f"{BASE_URL}register/", json=data)
        response.raise_for_status()
        result = response.json()
        global JOBSEEKER_TOKEN, EMPLOYER_TOKEN
        if data.get("is_employer"):
            EMPLOYER_TOKEN = result.get("token")
            print("Employer registration successful.")
        else:
            JOBSEEKER_TOKEN = result.get("token")
            print("Jobseeker registration successful.")
        print(result)
    except requests.RequestException as e:
        print(f"Registration failed: {e}")

def login():
    email = input("Enter email: ")
    password = input("Enter password: ")
    data = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(f"{BASE_URL}token/", json=data)
        response.raise_for_status()
        result = response.json()
        token = result.get("key")
        if token == JOBSEEKER_TOKEN:
            print("You are authorized to login")
            print("You logged in as a jobseeker")
        elif token == EMPLOYER_TOKEN:
            print("You are authorized to login")
            print("You logged in as an employer")
        else:
            print("You don't have an account")
            register_user()
    except requests.RequestException as e:
        print(f"Login failed: {e}")

def create_jobseeker_profile():
    if not JOBSEEKER_TOKEN:
        print ("Please login as a jobseeker first.")
        return
    
    print("Create Jobseeker Profile")
    first_name = input("Enter Your First Name: ")
    last_name = input("Enter Your Last Name: ")
    skills = input("Enter Your Skills: ")
    experience = input("Enter Your Year of Experience: ")
    phone_number = input("Enter Your Phone Number: ")

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "skills": skills,
        "experience": experience,
        "phone_number": phone_number
    }
    try:
        headers = {"Authorization": f"Token {JOBSEEKER_TOKEN}"}
        response = requests.post(f"{BASE_URL}jobseekers/", json=data, headers=headers)
        response.raise_for_status()
        print("Jobseeker profile created successfully.")
        print(response.json())
    except requests.RequestException as e:
        print(f"Failed to create jobseeker profile: {e}")

def create_employer_profile():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    print("Create Employer Profile")
    first_name = input("Enter Your First Name: ")
    last_name = input("Enter Your Last Name: ")
    location = input("Enter your street adress")
    phone_number = input("Enter Your Phone Number: ")

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "location": location,
        "phone_number": phone_number
    }

    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.post(f"{BASE_URL}employers/", json=data, headers=headers)
        response.raise_for_status()
        print("Employer profile created successfully.")
        print(response.json())
    except requests.RequestException as e:
        print(f"Failed to create employer profile: {e}")

def update_jobseeker_profile():
    if not JOBSEEKER_TOKEN:
        print("Please login as a jobseeker first.")
        return
    
    print("Update Jobseeker Profile")
    first_name = input("Enter New First Name: ")
    last_name = input("Enter New Last Name: ")
    skills = input("Enter New Skills: ")
    experience = input("Enter New Year of Experience: ")
    phone_number = input("Enter New Phone Number: ")

    data = {}
    if first_name:
        data["first_name"] = first_name
    if last_name:
        data["last_name"] = last_name
    if skills:
        data["skills"] = skills
    if experience:
        data["experience"] = experience
    if phone_number:
        data["phone_number"] = phone_number
    
    try:
        headers = {"Authorization": f"Token {JOBSEEKER_TOKEN}"}
        response = requests.patch(f"{BASE_URL}jobseekers/", json=data, headers=headers)
        response.raise_for_status()
        print("Jobseeker profile updated successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to update jobseeker profile: {e}")

def update_employer_profile():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    print("Update Employer Profile")
    first_name = input("Enter New First Name: ")
    last_name = input("Enter New Last Name: ")
    location = input("Enter New Street Address: ")
    phone_number = input("Enter New Phone Number: ")

    data = {}
    if first_name:
        data["first_name"] = first_name
    if last_name:
        data["last_name"] = last_name
    if location:
        data["location"] = location
    if phone_number:
        data["phone_number"] = phone_number
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.patch(f"{BASE_URL}employers/", json=data, headers=headers)
        response.raise_for_status()
        print("Employer profile updated successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to update employer profile: {e}")

def view_jobseeker_profile():
    if not JOBSEEKER_TOKEN:
        print("Please login as a jobseeker first.")
        return
    
    try:
        headers = {"Authorization": f"Token {JOBSEEKER_TOKEN}"}
        response = requests.get(f"{BASE_URL}jobseekers/", headers=headers)
        response.raise_for_status()
        print("Jobseeker Profile Details:")
        print(response.json())
    except requests.RequestException as e:
        print(f"Failed to retrieve jobseeker profile: {e}")

def view_employer_profile():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.get(f"{BASE_URL}employers/", headers=headers)
        response.raise_for_status()
        print("Employer Profile Details:")
        print(response.json())
    except requests.RequestException as e:
        print(f"Failed to retrieve employer profile: {e}")

def post_job():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    print("Post a Job")
    title = input("Enter job title: ")
    description = input("Enter job description: ")
    location = input("Enter job location: ")

    data = {
        "title": title,
        "description": description,
        "location": location
    }
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.post(f"{BASE_URL}job-posts/", json=data, headers=headers)
        response.raise_for_status()
        print("Job posted successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to post job: {e}")

def search_jobs():
    if not JOBSEEKER_TOKEN:
        print("Please login as a jobseeker first.")
        return
    
    print("Search for Jobs")
    search_term = input("Enter search term (leave blank for all jobs): ")
    
    try:
        headers = {"Authorization": f"Token {JOBSEEKER_TOKEN}"}
        params = {"search": search_term} if search_term else {}
        response = requests.get(f"{BASE_URL}job-posts/", headers=headers, params=params)
        response.raise_for_status()
        jobs = response.json()
        
        if not jobs:
            print("No jobs found.")
        else:
            for job in jobs:
                print(f"\nJob ID: {job['id']}")
                print(f"Title: {job['title']}")
                print(f"Description: {job['description']}")
                print(f"Location: {job['location']}")
                print(f"Skills Required: {job['skills_required']}")
                print(f"Experience Required: {job['experience_required']}")
    except requests.RequestException as e:
        print(f"Failed to search jobs: {e}")

def apply_for_job():
    if not JOBSEEKER_TOKEN:
        print("Please login as a jobseeker first.")
        return
    
    job_id = input("Enter the Job ID you want to apply for: ")
    
    try:
        headers = {"Authorization": f"Token {JOBSEEKER_TOKEN}"}
        response = requests.post(f"{BASE_URL}job-posts/{job_id}/apply/", headers=headers)
        response.raise_for_status()
        print("Application submitted successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to apply for job: {e}")

def view_applications():
    if JOBSEEKER_TOKEN:
        token = JOBSEEKER_TOKEN
        user_type = "jobseeker"
    elif EMPLOYER_TOKEN:
        token = EMPLOYER_TOKEN
        user_type = "employer"
    else:
        print("Please login first.")
        return
    
    try:
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(f"{BASE_URL}applications/", headers=headers)
        response.raise_for_status()
        applications = response.json()
        
        if not applications:
            print("No applications found.")
        else:
            for app in applications:
                print(f"\nApplication ID: {app['id']}")
                if user_type == "employer":
                    print(f"Applicant: {app['applicant']['email']}")
                print(f"Job: {app['job_post']['title']}")
                print(f"Status: {app['status']}")
                print(f"Applied at: {app['applied_at']}")
    except requests.RequestException as e:
        print(f"Failed to retrieve applications: {e}")

def rate_and_review_jobseeker():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    print("Rate and Review a Job Seeker")
    jobseeker_id = input("Enter the Job Seeker's ID: ")
    rating = input("Enter rating (1-5): ")
    comment = input("Enter your review comment: ")

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
    except ValueError:
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    data = {
        "rating": rating,
        "comment": comment
    }

    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.post(f"{BASE_URL}jobseekers/{jobseeker_id}/review/", json=data, headers=headers)
        response.raise_for_status()
        print("Review submitted successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to submit review: {e}")

def search_jobseekers():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    print("Search for Job Seekers")
    search_term = input("Enter skills to search for (comma-separated): ")
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        params = {"search": search_term} if search_term else {}
        response = requests.get(f"{BASE_URL}search-jobseekers/", headers=headers, params=params)
        response.raise_for_status()
        jobseekers = response.json()
        
        if not jobseekers:
            print("No job seekers found.")
        else:
            for js in jobseekers:
                print(f"\nJob Seeker ID: {js['id']}")
                print(f"Name: {js['first_name']} {js['last_name']}")
                print(f"Skills: {js['skills']}")
                print(f"Experience: {js['experience']}")
                if 'average_rating' in js:
                    print(f"Average Rating: {js['average_rating']:.2f}")
    except requests.RequestException as e:
        print(f"Failed to search job seekers: {e}")

def update_job_post():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    job_id = input("Enter the Job ID you want to update: ")
    print("Update Job Post (leave blank to keep current value)")
    title = input("Enter new job title: ")
    description = input("Enter new job description: ")
    location = input("Enter new job location: ")
    skills_required = input("Enter new required skills: ")
    experience_required = input("Enter new required experience: ")

    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if location:
        data["location"] = location
    if skills_required:
        data["skills_required"] = skills_required
    if experience_required:
        data["experience_required"] = experience_required
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.patch(f"{BASE_URL}job-posts/{job_id}/", json=data, headers=headers)
        response.raise_for_status()
        print("Job post updated successfully.")
        print("Response:", response.json())
    except requests.RequestException as e:
        print(f"Failed to update job post: {e}")

def delete_job_post():
    if not EMPLOYER_TOKEN:
        print("Please login as an employer first.")
        return
    
    job_id = input("Enter the Job ID you want to delete: ")
    
    try:
        headers = {"Authorization": f"Token {EMPLOYER_TOKEN}"}
        response = requests.delete(f"{BASE_URL}job-posts/{job_id}/", headers=headers)
        response.raise_for_status()
        print("Job post deleted successfully.")
    except requests.RequestException as e:
        print(f"Failed to delete job post: {e}")

def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Create Jobseeker Profile")
        print("4. Create Employer Profile")
        print("5. Update Jobseeker Profile")
        print("6. Update Employer Profile")
        print("7. View Jobseeker Profile")
        print("8. View Employer Profile")
        print("9. Post a Job")
        print("10. Search Jobs")
        print("11. Apply for a Job")
        print("12. View Applications")
        print("13. Search Job Seekers")
        print("14. Rate and Review a Job Seeker")
        print("15. Update Job Post")
        print("16. Delete Job Post")
        print("17. Exit")

        choice = input("Enter your Choice: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            login()
        elif choice == '3':
            create_jobseeker_profile()
        elif choice == '4':
            create_employer_profile()
        elif choice == '5':
            update_jobseeker_profile()
        elif choice == '6':
            update_employer_profile()
        elif choice == '7':
            view_jobseeker_profile()
        elif choice == '8':
            view_employer_profile()
        elif choice == '9':
            post_job()
        elif choice == '10':
            search_jobs()
        elif choice == '11':
            apply_for_job()
        elif choice == '12':
            view_applications()
        elif choice == '13':
            search_jobseekers()
        elif choice == '14':
            rate_and_review_jobseeker()
        elif choice == '15':
            update_job_post()
        elif choice == '16':
            delete_job_post()
        elif choice == '17':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
