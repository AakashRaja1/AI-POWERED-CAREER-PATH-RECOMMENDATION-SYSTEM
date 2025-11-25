<#
Simple PowerShell script to POST a sample payload to the running FastAPI /api/predict endpoint.
Usage:
  # from backend folder
  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test_predict.ps1

You can pass an alternate URL as the first positional argument.
#>
param(
    [string]$Url = 'http://127.0.0.1:8000/api/predict'
)

Write-Host "POSTing to: $Url"

$snake = @{ 
    user_id = "u123";
    full_name = "Test Student";
    education_level = "Bachelor's";
    academic_performance = "Above average";
    skills = "Python; SQL; Machine Learning";
    certifications = "";
    preference_data_people_ideas = "data";
    problem_solving_style = "Break problems into parts and prototype";
    structured_or_flexible = "structured";
    independent_or_team = "team";
    learning_style = "practice";
    interests = "Artificial Intelligence, Data Science";
    extra_curricular = "Coding Club";
}

$alias = @{ 
    "User ID" = "u123";
    "Full Name" = "Test Student";
    "Education Level" = "Bachelor's";
    "Academic Performance" = "Above average";
    "Skills" = "Python; SQL; Machine Learning";
    "Certifications" = "";
    "Do you prefer working with data, people, or ideas?" = "data";
    "How do you approach solving complex problems?" = "Break problems into parts and prototype";
    "Do you thrive better in a structured or flexible environment?" = "structured";
    "Do you prefer working independently or in a team?" = "team";
    "Do you learn best through practice, observation, or theory?" = "practice";
    "Interests" = "Artificial Intelligence, Data Science";
    "Extra-Curricular Activities" = "Coding Club";
}

function PostJson($payload) {
    $json = $payload | ConvertTo-Json -Depth 6
    try {
        $resp = Invoke-RestMethod -Uri $Url -Method Post -Body $json -ContentType 'application/json' -ErrorAction Stop
        Write-Host "Response (converted to JSON):"
        $resp | ConvertTo-Json -Depth 6
    } catch {
        Write-Host "Request failed:`n$($_.Exception.Message)"
        if ($_.Exception.Response -ne $null) {
            $task = $_.Exception.Response.Content.ReadAsStringAsync()
            $task.Wait()
            Write-Host "Response body:`n$($task.Result)"
        }
    }
}

Write-Host "--- Sending snake_case payload ---"
PostJson $snake

Write-Host "`n--- Sending alias-style payload ---"
PostJson $alias

Write-Host "Done"
