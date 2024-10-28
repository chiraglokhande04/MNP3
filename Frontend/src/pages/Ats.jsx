import React, { useState } from 'react';
import Navbar from '@/components/Navbar';
import FileUpload from '@/components/FileUpload';
import ResumeInfo from '@/components/ResumeInfo';

const Ats = () => {
  const [resumeData, setResumeData] = useState(null);

  // Function to handle successful file upload
  const handleUploadSuccess = (data) => {
    setResumeData(data); // Store the response data
  };

  // Function to reset resume data when uploading another resume
  const handleBackToUpload = () => {
    setResumeData(null); // Reset resume data
  };

  // Log the resumeData for debugging purposes
  console.log(resumeData);

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <div className="flex items-center justify-center flex-grow p-4">
        {!resumeData ? (
          <div className='flex flex-col items-center w-full max-w-lg'>
            <h1 className="text-5xl text-center font-poppins text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500 mt-10 animate-bounce">
              Check Your Resume Score !!!
            </h1>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : (
          <ResumeInfo
            resumeScore={resumeData.resume_score}
            candidateLevel={resumeData.cand_level}
            recommendedField={resumeData.recommended_field}
            recommendedSkills={resumeData.recommended_skills} // Use the array directly
            recommendedCourses={resumeData.recommended_courses} // Use the array directly
            onBackToUpload={handleBackToUpload} // Pass the function to ResumeInfo
          />
        )}
      </div>
    </div>
  );
};

export default Ats;
