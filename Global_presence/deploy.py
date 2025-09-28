import subprocess

PROJECT_ID = "{project_id}"  

FUNCTION_NAME = "global-presence"


REGIONS = [
    "us-central1",           # USA (Iowa)
    "europe-west1",          # Belgium
    "asia-east1",            # Taiwan
    "australia-southeast1",  # Australia
    "southamerica-east1",    # Brazil
    "asia-south1",           # India
]

def deploy_to_region(region):
    """Deploy the cloud function to a specific region"""
    function_name_with_region = f"{FUNCTION_NAME}-{region}"
    
    print(f"Deploying to {region}...")
    

    cmd = [
        "gcloud.cmd", "functions", "deploy", function_name_with_region,
        f"--region={region}",
        "--runtime=python311",
        "--trigger-http",
        "--allow-unauthenticated",
        "--entry-point=make_presence_request",
        f"--set-env-vars=FUNCTION_REGION={region}",
        f"--project={PROJECT_ID}",
        "--timeout=30s",
        "--memory=256MB",
        "--max-instances=10",
        "--no-gen2"
    ]
    
    try:
        # Run the deployment command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully deployed to {region}")
        return True
    except:
        print("Error")
        return False



def main():
    successful_deployments = 0
    
    # Deploy to each region
    for region in REGIONS:
        if deploy_to_region(region):
            successful_deployments += 1
        print("-" * 50)
        
    print(f'Successfully Deployed in {successful_deployments} regions')

if __name__ == "__main__":
    main()