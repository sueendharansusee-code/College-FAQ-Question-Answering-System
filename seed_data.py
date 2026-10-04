"""
Seed Data for College FAQ Question-Answering System.
Contains 9 categories and 36+ comprehensive sample FAQs.
"""

CATEGORIES = [
    {"name": "Admissions", "description": "Queries related to admission process, eligibility, cutoffs, and documents.", "icon": "fa-user-plus"},
    {"name": "Departments", "description": "Queries about academic departments, faculty, courses, and HOD contacts.", "icon": "fa-building-columns"},
    {"name": "Examination", "description": "Information on exam schedules, hall tickets, grading, and re-evaluation.", "icon": "fa-file-signature"},
    {"name": "Attendance", "description": "Rules regarding minimum attendance requirements, leave, and condonation.", "icon": "fa-clipboard-user"},
    {"name": "Library", "description": "Library timings, book borrowing limits, digital resources, and fines.", "icon": "fa-book-bookmark"},
    {"name": "Fees", "description": "Tuition fee structure, online payment options, deadlines, and refunds.", "icon": "fa-credit-card"},
    {"name": "Hostel", "description": "Hostel accommodation, mess timings, room allotment, and curfew rules.", "icon": "fa-hotel"},
    {"name": "Placements", "description": "Campus recruitment drive, eligibility criteria, training, and statistics.", "icon": "fa-briefcase"},
    {"name": "Campus", "description": "Facilities including Wi-Fi, canteen, medical center, transport, and sports.", "icon": "fa-graduation-cap"}
]

SAMPLE_FAQS = [
    # Admissions (4 entries)
    {
        "category": "Admissions",
        "question": "What is the undergraduate admission procedure?",
        "answer": "Undergraduate admissions are based on state/national entrance exam ranks followed by centralized counseling. Candidates must register online through the admissions portal, submit their 12th board marksheet, entrance scorecard, and participate in choice filling.",
        "keywords": "undergraduate ug admission procedure apply process entrance counseling selection eligibility criteria"
    },
    {
        "category": "Admissions",
        "question": "What documents are required during physical verification for admission?",
        "answer": "Required documents include: 10th & 12th Marksheets, Transfer Certificate (TC), Migration Certificate, Entrance Exam Scorecard, Category/Caste Certificate (if applicable), Income Certificate, Aadhaar Card, and 6 passport-size photographs.",
        "keywords": "documents required physical verification certificates marksheets TC migration passport photos checklist"
    },
    {
        "category": "Admissions",
        "question": "Are scholarship schemes available for deserving students?",
        "answer": "Yes! Merit-cum-means scholarships, state government reservation scholarships, and single-girl child assistance are available. Students can apply through the National Scholarship Portal (NSP) or the College Financial Aid cell in Block A.",
        "keywords": "scholarship financial aid tuition waiver merit means NSP grant assistance concession"
    },
    {
        "category": "Admissions",
        "question": "What is the deadline for submitting online admission applications?",
        "answer": "The deadline for undergraduate application submission is July 15th for Phase 1 and August 5th for Phase 2. Post-graduate applications close on July 30th.",
        "keywords": "deadline last date submission online admission form application close cutoff timing"
    },

    # Departments (4 entries)
    {
        "category": "Departments",
        "question": "Which academic departments and courses are offered by the college?",
        "answer": "The college offers undergraduate and postgraduate degrees across 6 main departments: Computer Science & Engineering, Electronics & Communication, Mechanical Engineering, Civil Engineering, Business Administration (MBA/BBA), and Applied Sciences.",
        "keywords": "departments streams courses programs degrees branches CSE ECE Mechanical Civil Management MBA BBA"
    },
    {
        "category": "Departments",
        "question": "How can I contact the Head of Department (HOD)?",
        "answer": "HOD contact details and official email addresses are listed under the respective department tab on the college website. You can also visit their office in the Main Academic Block during office hours (2:00 PM to 4:00 PM on weekdays).",
        "keywords": "contact HOD head of department office email meet appointment consultation visiting hours"
    },
    {
        "category": "Departments",
        "question": "Is branch transfer or change permitted after the first year?",
        "answer": "Yes, branch transfer is permitted after the 2nd semester, subject to seat availability in the target department and a minimum CGPA of 8.5 in the first year without any active backlogs.",
        "keywords": "branch transfer change department switch major stream first year CGPA criteria eligibility"
    },
    {
        "category": "Departments",
        "question": "What specialized research labs are available in the Computer Science department?",
        "answer": "The CSE department houses specialized labs for Artificial Intelligence & Machine Learning, Data Science, Cyber Security, IoT & Embedded Systems, and Cloud Computing, equipped with high-performance GPU workstations.",
        "keywords": "laboratories labs research AI ML machine learning cyber security data science cloud GPU CSE department"
    },

    # Examination (4 entries)
    {
        "category": "Examination",
        "question": "Where can I find the end-semester examination schedule and time table?",
        "answer": "The official examination timetable is published 3 weeks prior to exams on the Controller of Examinations (COE) portal and posted on departmental notice boards. You can also download it from the student portal.",
        "keywords": "exam schedule examination time table end semester datesheet COE portal dates when exam start"
    },
    {
        "category": "Examination",
        "question": "How do I download my hall ticket or admit card for semester exams?",
        "answer": "Log in to the Student ERP portal using your Roll Number, navigate to the 'Examinations' tab, select 'Admit Card', and click download. Ensure all outstanding tuition fees are cleared to enable ticket download.",
        "keywords": "hall ticket admit card download exam permission roll number student ERP exam portal"
    },
    {
        "category": "Examination",
        "question": "What is the procedure for answer script re-evaluation or re-checking?",
        "answer": "Students dissatisfied with their exam marks can apply for re-evaluation within 10 days of result publication via the ERP portal. A fee of $15 (or Rs. 500) per subject is applicable. Evaluated answer sheets can also be inspected.",
        "keywords": "revaluation re-evaluation rechecking marks challenge result paper inspection grade improvement"
    },
    {
        "category": "Examination",
        "question": "How do supplementary or backlog examinations work?",
        "answer": "Supplementary exams are held twice a year (during summer break and winter break). Registration opens 15 days after main exam results. A maximum of 4 backlog papers can be attempted per supplementary session.",
        "keywords": "supplementary backlog compartment fail exam re-appear repeat paper registration arrear"
    },

    # Attendance (4 entries)
    {
        "category": "Attendance",
        "question": "What is the minimum attendance percentage required to sit for semester examinations?",
        "answer": "A minimum of 75% attendance in both theory lectures and practical labs is mandatory to be eligible for end-semester examinations. Students with attendance between 65% and 74% require medical condonation.",
        "keywords": "minimum attendance percentage requirement 75 percent eligible exam rule mandatory criteria"
    },
    {
        "category": "Attendance",
        "question": "How do I apply for medical leave or condonation of attendance shortage?",
        "answer": "Submit a formal leave application along with a valid Medical Certificate signed by a registered practitioner to your Class Advisor within 3 working days of resuming classes. Upon approval by the Dean, condonation of up to 10% may be granted.",
        "keywords": "medical leave apply condonation shortage illness hospital doctor certificate approval attendance waiver"
    },
    {
        "category": "Attendance",
        "question": "Where can students track their daily subject-wise attendance?",
        "answer": "Students can track real-time attendance on the official Mobile App or Student ERP portal under 'Attendance Summary'. Class advisors update attendance daily by 5:00 PM.",
        "keywords": "track check attendance daily percentage summary ERP app view portal status subject-wise"
    },
    {
        "category": "Attendance",
        "question": "What happens if a student has less than 65% attendance?",
        "answer": "Students with less than 65% attendance are detained (condonation not applicable) and will not be permitted to take the end-semester exams for those subjects. They must re-register for the course in subsequent semesters.",
        "keywords": "detained shortage low attendance below 65 percent bar exam repeat course penalty consequences"
    },

    # Library (4 entries)
    {
        "category": "Library",
        "question": "What are the central library working hours and timings?",
        "answer": "The Central Library is open Monday through Saturday from 8:00 AM to 10:00 PM. During semester examinations, extended reading room hours operate 24/7. On Sundays and public holidays, it functions from 9:00 AM to 5:00 PM.",
        "keywords": "library hours timings open close weekends examination reading room night central library"
    },
    {
        "category": "Library",
        "question": "How many books can an undergraduate student borrow and for how long?",
        "answer": "Undergraduate students can borrow up to 4 books for a duration of 14 days. Postgraduate students can borrow 6 books for 21 days. Books can be renewed online once if not reserved by another user.",
        "keywords": "borrow books library limit duration days how many issue renew return policy"
    },
    {
        "category": "Library",
        "question": "How do I access IEEE, Springer, and digital journal subscriptions?",
        "answer": "Digital library e-resources (IEEE Xplore, ScienceDirect, Springer, ACM) are accessible on campus via the college Wi-Fi network. For remote off-campus access, login via the KNIMBUS Remote Access portal using your college email.",
        "keywords": "digital library IEEE Springer journals research papers e-books electronic resources remote access IP"
    },
    {
        "category": "Library",
        "question": "What is the penalty fine for overdue books?",
        "answer": "A late fine of Rs. 5 ($0.10) per day per book is charged for overdue returns. If a book is lost, the student must replace the book (latest edition) or pay double the market cost of the book.",
        "keywords": "fine penalty overdue late return book loss charge per day library card"
    },

    # Fees (4 entries)
    {
        "category": "Fees",
        "question": "What are the accepted modes of fee payment and online portals?",
        "answer": "Fees can be paid online via Net Banking, UPI, Credit/Debit cards through the Student ERP portal (SBI Collect / HDFC Gateway). Offline payments are accepted via Demand Draft (DD) favoring 'The Registrar, College Account'. Cash is not accepted.",
        "keywords": "fee payment payment mode online portal UPI netbanking credit card DD demand draft SBI collect"
    },
    {
        "category": "Fees",
        "question": "What is the fee structure for hostel, tuition, and examination?",
        "answer": "Annual tuition fees range between $1,200 - $2,500 depending on the branch. Hostel fee is $800/year (including mess charges). Semester examination fee is $30 per semester. Detailed breakdown is available on the Accounts tab of the ERP portal.",
        "keywords": "fee structure tuition fee cost breakdown annual total how much hostel mess exam fee charge"
    },
    {
        "category": "Fees",
        "question": "What is the last date to pay semester tuition fees without a late fine?",
        "answer": "Semester tuition fees must be paid within 15 days from the start of the semester. A grace period of 7 days is provided, after which a late fine of Rs. 100 per day is levied up to a maximum of 30 days.",
        "keywords": "last date fee payment deadline grace period late fee fine due date deadline"
    },
    {
        "category": "Fees",
        "question": "What is the fee refund policy in case of admission cancellation?",
        "answer": "If admission is cancelled before the official start of classes, 90% of tuition fee is refunded after deducting a $20 processing charge. If cancelled within 15 days after classes start, 50% is refunded. No refund is granted after 30 days.",
        "keywords": "refund policy admission cancellation withdraw money return percentage rules processing fee"
    },

    # Hostel (4 entries)
    {
        "category": "Hostel",
        "question": "How is hostel accommodation allocated to new students?",
        "answer": "Hostel rooms are allocated on a first-come, first-served basis during admission counseling. Outstation candidates from beyond 50 km are given priority. Both single, double, and triple-sharing rooms with air-conditioning options are available.",
        "keywords": "hostel accommodation room allocation allotment single double sharing AC non-AC outstation priority stay"
    },
    {
        "category": "Hostel",
        "question": "What are the hostel night curfew timings and outing rules?",
        "answer": "The evening curfew time for all resident students is 9:30 PM. Outpass for weekend leave or local outings must be requested 24 hours prior through the Hostel Management Mobile App and approved by the Warden.",
        "keywords": "hostel curfew night timing entry exit outpass Warden gate timing evening permission outing rules"
    },
    {
        "category": "Hostel",
        "question": "What are the hostel mess timings and meal plans offered?",
        "answer": "The mess serves 4 meals daily: Breakfast (7:30 AM - 9:00 AM), Lunch (12:30 PM - 2:00 PM), Evening Snacks (5:00 PM - 6:00 PM), and Dinner (7:30 PM - 9:30 PM). A balanced vegetarian and non-vegetarian (3 days/week) menu is curated by the student mess committee.",
        "keywords": "mess timings food meals breakfast lunch dinner non-veg veg quality food menu hostel dining"
    },
    {
        "category": "Hostel",
        "question": "What laundry and room facilities are provided in the hostel?",
        "answer": "Each room is furnished with a study table, chair, wardrobe, and bed with mattress. Automated laundry facility (up to 15 kg/month included), 24/7 power backup, solar water heaters, and high-speed Wi-Fi access are provided.",
        "keywords": "hostel facilities laundry washing machine bed table furniture power backup Wi-Fi hot water amenities"
    },

    # Placements (4 entries)
    {
        "category": "Placements",
        "question": "What is the placement record and average salary package of the college?",
        "answer": "The college maintains a stellar 92%+ placement rate for eligible engineering graduates. The highest international package offered last year was $65,000 (Rs. 52 LPA), while the average salary package across branches is $8,500 (Rs. 7.2 LPA).",
        "keywords": "placement record average salary package highest package placement percentage statistics recruiters placements"
    },
    {
        "category": "Placements",
        "question": "Which top companies visit the campus for recruitment drives?",
        "answer": "Over 150+ top tier companies recruit on campus, including TCS, Infosys, Wipro, Amazon, Microsoft, Accenture, Cognizant, Deloitte, L&T, and Tata Motors.",
        "keywords": "top companies recruitment recruiters visiting campus Amazon Microsoft TCS Infosys Wipro hiring firms"
    },
    {
        "category": "Placements",
        "question": "What are the eligibility criteria for participating in campus placements?",
        "answer": "Students must possess a minimum CGPA of 6.0 (60%) throughout 10th, 12th, and B.Tech without active backlogs at the time of recruitment drives. Attendance in Placement Training Sessions is mandatory.",
        "keywords": "placement eligibility CGPA criteria backlogs percentage training placement drive qualification rules"
    },
    {
        "category": "Placements",
        "question": "Does the Training and Placement Cell (T&P) offer soft skill training and mock interviews?",
        "answer": "Yes! The Placement Cell conducts soft skills workshops, quantitative aptitude training, coding bootcamp, resume writing sessions, and mock technical & HR interviews starting from the 5th semester.",
        "keywords": "training placement cell soft skills mock interviews aptitude coding bootcamp resume workshop preparation"
    },

    # Campus (4 entries)
    {
        "category": "Campus",
        "question": "How do students access the high-speed campus Wi-Fi network?",
        "answer": "Connect to the 'College-Student-WiFi' network using your campus ERP credentials (roll number as username). Each student is allotted 100 GB high-speed monthly data quota across 2 registered devices.",
        "keywords": "campus Wi-Fi internet connect login password network quota speed wifi access data limit"
    },
    {
        "category": "Campus",
        "question": "What medical and health facilities are available on campus?",
        "answer": "A 24/7 Health Center with full-time resident medical officer, emergency nursing staff, and a dedicated college ambulance is available near the Sports Complex. Basic consultation and medicines are free for students.",
        "keywords": "medical clinic health center doctor emergency ambulance hospital health doctor nurse medicine campus"
    },
    {
        "category": "Campus",
        "question": "What sports and fitness facilities are present on campus?",
        "answer": "The campus boasts an Olympic-size swimming pool, indoor sports complex (badminton, table tennis, squash), basketball courts, cricket ground, football turf, and a fully equipped gymnasium with certified trainers.",
        "keywords": "sports fitness gymnasium gym swimming pool cricket ground basketball badminton games ground"
    },
    {
        "category": "Campus",
        "question": "What food outlets and canteen options are available inside campus?",
        "answer": "Besides the central multi-cuisine student cafeteria, campus options include Cafe Coffee Day express, Subway kiosk, Amul parlor, fruit juice center, and a 24-hour food court in the student activity center.",
        "keywords": "canteen cafeteria food court coffee cafe dining snacks eating outlets food spots inside campus"
    }
]

SUGGESTED_QUESTIONS = [
    "What is the minimum attendance requirement?",
    "How can I apply for medical leave?",
    "What are the hostel fee structures and mess timings?",
    "How to download my exam hall ticket?",
    "What is the undergraduate admission procedure?",
    "What is the average placement salary package?",
    "What are the central library working hours?",
    "How do I connect to the campus Wi-Fi?"
]
