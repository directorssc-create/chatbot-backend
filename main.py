import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
from rapidfuzz import fuzz

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ==========================================
# 1. TRANSLATION SETUP
# ==========================================
def translate_to_english(text):
    """Translates Hindi/Hinglish queries to English for uniform processing."""
    if not text or not str(text).strip():
        return text
    try:
        translator = GoogleTranslator(source='auto', target='en')
        translated = translator.translate(str(text))
        return translated if translated else text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

# ==========================================
# 2. EXPANDED IGNOU FAQ DATABASE
# ==========================================
RAW_FAQS = [
    # --- 1. ADMISSION ---
    {
        "keywords": ['new admission', 'ignou admission process', 'apply online', 'admission form', 'registration', 'january session', 'july session'],
        "question": 'How can I take admission in IGNOU?',
        "answer": 'IGNOU offers admission to various programmes twice a year, in the January and July sessions. Once the University announces the admission session, visit the official admission portal, select the appropriate programme, verify eligibility, and apply for fresh admission. The admission process is entirely online; applications submitted offline or by post are not accepted.',
        "category": 'Admission'
    },
    {
        "keywords": ['procedure online admission', 'create user id', 'upload documents', 'admission portal', 'new registration'],
        "question": 'What is the procedure for online admission?',
        "answer": "Visit the admission portal and click 'New Registration' to create a user ID and password. After logging in, fill in the required details in the application form and upload your photograph, signature and educational certificates in the prescribed format. Pay the fee through the available payment gateway and confirm the payment status. Once the documents have been verified, the University confirms the admission.",
        "category": 'Admission'
    },
    {
        "keywords": ['admission status', 'enrollment number', 'check admission status', 'discrepancy'],
        "question": 'How can I check the status of my admission?',
        "answer": 'Use the official admission/student portal and its registration-status facility. If a discrepancy persists, contact the concerned Regional Centre or the Student Registration Division support channel.',
        "category": 'Admission'
    },
    {
        "keywords": ['wrong mobile number', 'incorrect email', 'update contact details', 'change phone number'],
        "question": 'What should I do if my registered mobile number or e-mail address is incorrect?',
        "answer": 'Approach the concerned Regional Centre to update or correct your registered mobile number and/or e-mail address. Correct contact details are essential for receiving OTPs, confirmations and important University communications.',
        "category": 'Admission'
    },
    {
        "keywords": ['change programme', 'change regional centre', 'update registration details'],
        "question": 'Can I change my programme, Regional Centre or other registration details?',
        "answer": "Such changes are subject to the University's prescribed rules and procedures. Use the designated online facility where available, or contact the concerned IGNOU office/Regional Centre with supporting documents.",
        "category": 'Admission'
    },
    {
        "keywords": ['printed copy application', 'submit hard copy regional centre', 'post application'],
        "question": 'After making the payment, do I need to submit a printed copy of the application form to the Regional Centre?',
        "answer": 'No. The entire process is completed online, and there is no need to submit a printed copy at the Regional Centre.',
        "category": 'Admission'
    },
    {
        "keywords": ['download id card', 'identity card', 'laminated id card', 'digitally attested id'],
        "question": 'How do I download my Identity (ID) Card?',
        "answer": "Once admission is confirmed, you'll receive an email and SMS notification. Log in to the admission portal and download your ID card via 'Download ID Card', print in colour and get it laminated. No attestation visit is needed — the card is digitally attested.",
        "category": 'Admission'
    },
    {
        "keywords": ['after admission confirmed', 'induction meeting', 'march april september october'],
        "question": 'What should I do after my admission is confirmed?',
        "answer": 'Check your admission dashboard regularly and attend the Induction Meeting, held in March–April for the January session and September–October for the July session. A recorded video is posted if you miss it.',
        "category": 'Admission'
    },

    # --- 2. RE-REGISTRATION ---
    {
        "keywords": ['what is re-registration', 'next semester registration', 'next year admission', 'reregistration'],
        "question": 'What is re-registration?',
        "answer": 'For semester- or annual-system programmes, students must complete re-registration to continue into the next semester/year. This is independent of whether you appeared in, or passed, your current courses.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['wait previous examination result', 'reregister before result', 're-registration result wait'],
        "question": 'Do I have to wait for my previous examination result before re-registering?',
        "answer": 'No. Students may generally re-register for the next semester/year without waiting for the previous examination result. Follow the notified re-registration schedule.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['re-register without assignment', 'reregistration without exam', 'earlier assignments pending'],
        "question": 'Can I re-register if I have not submitted assignments or appeared in the previous examination?',
        "answer": 'Yes, re-registration is generally not conditional on completing earlier assignments or examinations. However, all academic requirements must be fulfilled within the programme\'s prescribed validity period.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['apply re-registration', 're-registration portal', 're-registration process'],
        "question": 'How do I apply for re-registration?',
        "answer": 'The entire process is completed online through the designated re-registration portal, as per the schedule notified by the University. Select the eligible courses, verify the information, accept the declaration, pay the prescribed fee, and retain the confirmation/receipt.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['cannot receive otp', 'otp issue reregistration', 'mobile email otp'],
        "question": 'What should I do if I cannot receive the OTP while registering?',
        "answer": 'First verify that your registered mobile number and e-mail address are correct. If the issue continues, contact the concerned Regional Centre for assistance.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['confirm re-registration success', '20 days reregistration', 'reregistration status'],
        "question": 'How can I confirm that my re-registration was completed successfully?',
        "answer": 'It generally reflects in your registration details within about 20 days of application — check your account periodically.',
        "category": 'Re-registration'
    },
    {
        "keywords": ['re-registration issues contact', 'reregistration helpdesk', 'reregister support'],
        "question": 'Whom should I contact for issues relating to re-registration?',
        "answer": 'Contact your Regional Centre by email, or write to the designated student registration support address.',
        "category": 'Re-registration'
    },

    # --- 3. STUDY MATERIAL ---
    {
        "keywords": ['receive study material', 'mpdd postal delivery', 'books dispatch duration'],
        "question": 'When and how will I receive study material after admission?',
        "answer": "It is dispatched by the University's Material Production and Distribution Division (MPDD) to your registered postal address, generally taking one to two months.",
        "category": 'Study Material'
    },
    {
        "keywords": ['soft copy study material', 'egyankosh pdf', 'mobile app books'],
        "question": 'Is a soft copy of the study material available?',
        "answer": "Yes, free of charge on the University's e-content/eGyanKosh platform and the corresponding mobile application.",
        "category": 'Study Material'
    },
    {
        "keywords": ['track dispatch status', 'mpdd tracking', 'books status tracking'],
        "question": 'How can I track the dispatch status of my study material?',
        "answer": "Through the MPDD section on the University's website.",
        "category": 'Study Material'
    },
    {
        "keywords": ['did not receive study material', 'books not arrived', 'material distribution unit contact'],
        "question": 'What should I do if I do not receive my study material?',
        "answer": 'First verify your admission confirmation, registered address and material dispatch status. If it still hasn\'t arrived, contact the concerned Regional Centre or Material Distribution Unit through the prescribed channel.',
        "category": 'Study Material'
    },
    {
        "keywords": ['opted soft copy now need hard copy', 'convert soft copy to hard copy', 'registrar mpdd fee'],
        "question": 'I opted for a soft copy but now need a hard copy — what do I do?',
        "answer": 'Send a request letter with the prescribed fee to the Registrar, MPDD, IGNOU, Maidan Garhi, New Delhi. The price list is on the University website.',
        "category": 'Study Material'
    },

    # --- 4. ACADEMIC COUNSELLING ---
    {
        "keywords": ['academic counselling location', 'study centre classes', 'learner support centre counselling'],
        "question": 'Where are academic counselling sessions conducted?',
        "answer": 'Academic counselling is organised through the learner-support network — designated Learner Support Centres/Study Centres — according to the programme and schedule. Check the counselling schedule issued by your centre.',
        "category": 'Academic Counselling'
    },
    {
        "keywords": ['compulsory counselling', 'mandatory practicals', 'theory optional practical compulsory'],
        "question": 'Is it compulsory to attend counselling sessions?',
        "answer": 'Theory sessions are optional, but practical counselling sessions are mandatory — required for eligibility in the practical exam and viva-voce.',
        "category": 'Academic Counselling'
    },
    {
        "keywords": ['missed online counselling', 'recorded videos counselling', 'elearning platform videos'],
        "question": 'If I miss an online counselling session, are recorded videos available?',
        "answer": "Yes, recorded videos are typically posted on the University's e-learning platform.",
        "category": 'Academic Counselling'
    },

    # --- 5. ASSIGNMENTS ---
    {
        "keywords": ['assignment download', 'assignment question paper', 'ignou assignment pdf', 'get assignment'],
        "question": 'Where can I obtain assignment question papers?',
        "answer": 'Assignment question papers are available on the official IGNOU website and the designated assignment portal. Download the assignment applicable to your programme, course code and academic session.',
        "category": 'Assignments'
    },
    {
        "keywords": ['why assignments important', 'continuous evaluation', 'assignment marks weightage'],
        "question": 'Why are assignments important?',
        "answer": 'Assignments are an integral part of continuous evaluation in applicable programmes. Their marks contribute to the overall assessment as per the evaluation scheme prescribed for the concerned programme/course.',
        "category": 'Assignments'
    },
    {
        "keywords": ['where to submit assignments', 'study centre assignment submission', 'hard copy assignment'],
        "question": 'Where should I submit my assignments?',
        "answer": 'Hard copies of hand-written assignments must be submitted at the concerned study centre, either in person or by post. Assignments sent by email are not accepted, unless the current instructions for your programme state otherwise.',
        "category": 'Assignments'
    },
    {
        "keywords": ['submit assignments online', 'online assignment mode', 'learner support centre rules'],
        "question": 'Can I submit assignments online?',
        "answer": 'The submission mode depends on the instructions issued for your programme, course and Learner Support Centre. Always follow the currently applicable University instructions rather than an older practice.',
        "category": 'Assignments'
    },
    {
        "keywords": ['assignment last date', 'assignment deadline', '31 march 30 september assignment'],
        "question": 'What is the last date for submitting assignments?',
        "answer": 'Generally 31 March for the June term-end examination and 30 September for the December term-end examination. Any extension is announced on the University\'s website and social media.',
        "category": 'Assignments'
    },
    {
        "keywords": ['typed assignments', 'handwritten assignments', 'printed assignment acceptable'],
        "question": 'Are typed assignments acceptable?',
        "answer": 'No, assignments must be hand-written only unless specifically instructed otherwise for your programme. Typed assignments are generally not evaluated.',
        "category": 'Assignments'
    },
    {
        "keywords": ['assignment cover page', 'enrolment number on assignment', 'assignment cover details'],
        "question": 'Can I submit an assignment without writing my enrolment number and other details?',
        "answer": 'No — follow the prescribed assignment cover-page and submission instructions, and clearly mention all required identification details. Incomplete identification may cause difficulty in processing your submission.',
        "category": 'Assignments'
    },
    {
        "keywords": ['single file all assignments', 'separate assignment file', 'spiral binding assignment'],
        "question": 'Can assignments for all courses be submitted in a single file?',
        "answer": 'No — a separate file or spiral binding per course, with a cover page stating name, enrolment number, course code, programme and study centre, plus a copy of the question paper.',
        "category": 'Assignments'
    },
    {
        "keywords": ['assignment submission compulsory', 'assignment necessary for tee', 'exam eligibility assignment'],
        "question": 'Is submission of assignments compulsory?',
        "answer": 'Yes — without it you are not eligible to appear in the term-end examination.',
        "category": 'Assignments'
    },
    {
        "keywords": ['assignment not available online', 'missing assignment paper', 'course coordinator contact'],
        "question": 'What should I do if an assignment is not available online?',
        "answer": 'First verify the programme and course code you searched. If it\'s still unavailable, contact the concerned School of Study/Course Coordinator or your Regional Centre through the prescribed channel.',
        "category": 'Assignments'
    },
    {
        "keywords": ['fail in assignment', 'assignment revaluation', 'fresh assignment submit'],
        "question": 'What if I don\'t get a pass mark/grade in an assignment?',
        "answer": 'Submit a fresh assignment based on the latest question paper for the next cycle. There is generally no provision for revaluation of assignments.',
        "category": 'Assignments'
    },
    {
        "keywords": ['assignment submission receipt', 'post office receipt assignment', 'assignment proof'],
        "question": 'Should I keep a receipt after submitting my assignments?',
        "answer": 'Yes — collect a receipt in person, or keep the post office receipt if mailed. Also keep a photocopy/scan until results are declared.',
        "category": 'Assignments'
    },

    # --- 6. TERM-END EXAMINATION (TEE) ---
    {
        "keywords": ['how many times tee conducted', 'june december tee', 'exam frequency'],
        "question": 'How many times a year is the term-end examination conducted?',
        "answer": 'Twice a year — June and December. January-session (annual programme) students sit December; July-session students sit June, subject to the University\'s notified schedule.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['procedure appearing examination', 'exam form online', 'tee fee payment'],
        "question": 'What is the procedure for appearing in the examination?',
        "answer": 'Submit assignments for the relevant courses first, then submit the online examination form within the notified period, select the eligible courses, complete the required declarations, and pay the prescribed examination fee per subject.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['appear exam result pending', 'exam form pending result', 'earlier results undeclared'],
        "question": 'Can I appear for an examination if my previous result has not yet been declared?',
        "answer": 'Where permitted by the examination instructions, you may submit the exam form for eligible courses without waiting for all earlier results. Follow the current examination notification carefully.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['clash exam date', 'two exams same time slot', 'exam conflict'],
        "question": 'Can I appear for two examinations scheduled at the same time?',
        "answer": 'No. You cannot write examinations for two courses in the same session/time slot, even if both appear on your hall ticket for that session.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['change examination centre', 'exam center change', 'centre allotment change'],
        "question": 'Can I change my examination centre after allotment?',
        "answer": 'Centre changes are governed by the current examination instructions. Read the relevant notification carefully, as such requests may be restricted after final allotment.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['admission fee exam fee included', 'separate exam fee', 'tee fee extra'],
        "question": 'Does the admission fee include the examination fee?',
        "answer": 'No — only the admission fee is charged at admission. The examination fee is paid separately.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['exam fee refund', 'exam fee carry forward', 'fee refund non appearance'],
        "question": 'If I pay the exam fee but don\'t appear, is it refunded or carried forward?',
        "answer": 'No, once paid it is neither refunded nor carried forward to the next cycle.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['exam centre outside regional centre', 'choose exam centre anywhere india'],
        "question": 'Can I choose an examination centre outside my Regional Centre?',
        "answer": 'Yes, for the theory term-end exam you may generally choose any centre in India while filling the exam form.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['minimum study period tee', '11 months annual 5 months semester', 'eligibility term end exam'],
        "question": 'What is the minimum study period to become eligible for the term-end exam?',
        "answer": '11 months for annual programmes; 5 months for semester/certificate programmes.',
        "category": 'Term-End Examination'
    },
    {
        "keywords": ['tentative date sheet', 'exam date time', 'hall ticket release date'],
        "question": 'How will I know the date and time of my examination?',
        "answer": 'A tentative date sheet is uploaded roughly 60 days before the exam, followed by the hall ticket stating date, time, session and centre address — downloadable from the website.',
        "category": 'Term-End Examination'
    },

    # --- 7. HALL TICKET, CONDUCT & UNFAIR MEANS ---
    {
        "keywords": ['hall ticket unavailable', 'admit card not found', 'download hall ticket issue'],
        "question": 'What should I do if my examination hall ticket is not available?',
        "answer": 'Verify your examination form/payment status, course eligibility and University updates. If the hall ticket is still unavailable after the University publishes it, contact the concerned Regional Centre/Examination Division through the prescribed channel.',
        "category": 'Hall Ticket & Conduct'
    },
    {
        "keywords": ['carry to exam hall', 'hall ticket and id card', 'required items exam center'],
        "question": 'What must I carry to the examination hall?',
        "answer": 'Your hall ticket and, if possible, your IGNOU ID card — without these you won\'t be permitted to appear.',
        "category": 'Hall Ticket & Conduct'
    },
    {
        "keywords": ['exam writing language', 'hindi language exam option', 'medium of examination'],
        "question": 'In which language can I write my examination?',
        "answer": 'Write your answers in the language permitted for the concerned programme/course. IGNOU\'s examination instructions may permit Hindi for certain courses even where you are registered in English, subject to programme-specific exceptions, particularly language programmes.',
        "category": 'Hall Ticket & Conduct'
    },
    {
        "keywords": ['unfair means ufm', 'cheating in exam', 'prohibited activities exam hall'],
        "question": 'What happens if a student uses unfair means?',
        "answer": 'Unfair means in examinations are dealt with under the applicable University rules and statutes. Strictly comply with examination instructions and do not engage in any prohibited activity.',
        "category": 'Hall Ticket & Conduct'
    },

    # --- 8. RESULTS & GRADE CARD ---
    {
        "keywords": ['check examination result', 'ignou result link', 'enrolment number result'],
        "question": 'Where can I check my examination result?',
        "answer": 'Use the official IGNOU result facility and verify the result using your prescribed student/enrolment details.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['result declaration timeline', '45 days exam result', 'tee result date'],
        "question": 'When is the result of the term-end examination declared?',
        "answer": 'Results are generally declared within 45 days from the date of completion of the last examination.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['result not showing', 'pending exam result', 'phased result publication'],
        "question": 'Why is my result not showing even though I appeared in the examination?',
        "answer": 'Results may be processed and uploaded in phases. First verify whether the result for that course has been declared. If it remains pending beyond the usual processing period, raise the matter through the prescribed University support/grievance mechanism.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['what is grade card', 'grade card performance', 'assignment and exam status'],
        "question": 'What is a grade card?',
        "answer": 'The grade card records your academic performance/status for the components applicable to your programme, such as assignments and term-end examinations, as applicable.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['missing assignment marks', 'missing practical marks', 'marks not updated grade card'],
        "question": 'What should I do if assignment, practical or project marks are missing?',
        "answer": 'First verify your submission status and the applicable evaluation process. If marks are still not reflected, contact the concerned Regional Centre/Learner Support Centre or the relevant Evaluation Division with proof of submission, where required.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['provisional certificate dispatch', 'marksheet receipt', 'registered post marksheet'],
        "question": 'When will I receive my mark sheet and provisional certificate?',
        "answer": 'IGNOU does not issue year- or semester-wise mark sheets. These are issued only after the entire programme is completed, sent by Registered Post to your registered address.',
        "category": 'Results & Grade Card'
    },
    {
        "keywords": ['student portal login', 'forgot password ignou portal', 'reset portal password'],
        "question": 'What do I need to log in to the student portal, and what if I forget my password?',
        "answer": "You need your enrolment number, programme code and password. If you forget your password, use 'Forgot Password' on the login page and reset it using your enrolment number and registered email/date of birth.",
        "category": 'Results & Grade Card'
    },

    # --- 9. RE-EVALUATION & ANSWER SCRIPTS ---
    {
        "keywords": ['re-evaluation apply', 'reevaluation deadline', 'higher marks revaluation'],
        "question": 'Can I apply for re-evaluation of my answer script?',
        "answer": 'Where re-evaluation is permitted for the concerned examination/course, apply within the prescribed period through the designated process — before 31 March for the December TEE, or 30 September for the June TEE, or within one month of the result being declared, whichever is later. Consult the applicable notification for eligibility, fee and procedure. After re-evaluation, the higher of the original and revalued marks/grade is considered. Re-evaluation generally applies only to the theory term-end examination, not to project/dissertation, practical/lab courses, workshops or assignments.',
        "category": 'Re-evaluation'
    },
    {
        "keywords": ['copy of evaluated answer script', 'scanned answer script', 'photocopy answer sheet'],
        "question": 'Can I obtain a copy of my evaluated answer script?',
        "answer": 'IGNOU provides a prescribed mechanism for obtaining a copy or scanned copy of answer scripts, subject to applicable rules, timelines and fees. Use the official facility notified for the relevant examination.',
        "category": 'Re-evaluation'
    },

    # --- 10. PROJECTS & PRACTICALS ---
    {
        "keywords": ['project synopsis guidelines', 'dissertation rules', 'project guidelines ignou'],
        "question": 'Where can I find project/synopsis guidelines?',
        "answer": 'Consult the official programme guide, project guidelines, and the instructions issued by the concerned School of Study/Regional Centre. Follow the programme-specific formats, submission windows and approval requirements.',
        "category": 'Projects & Practicals'
    },
    {
        "keywords": ['project approval contact', 'project supervisor', 'submit dissertation'],
        "question": 'Whom should I contact regarding project approval or submission?',
        "answer": 'Depending on your programme\'s prescribed workflow, contact the Regional Centre, Learner Support Centre, School of Study, Programme Coordinator, or your designated project supervisor.',
        "category": 'Projects & Practicals'
    },
    {
        "keywords": ['are practicals compulsory', 'practical component mandatory', 'lab work requirements'],
        "question": 'Are practicals compulsory?',
        "answer": 'Where a programme/course contains practical components, students must fulfil the prescribed practical requirements in accordance with the programme structure and University instructions.',
        "category": 'Projects & Practicals'
    },

    # --- 11. DEGREE, TRANSCRIPT & DIGILOCKER ---
    {
        "keywords": ['eligible final qualification award', 'degree completion conditions', 'programme duration validity'],
        "question": 'When is a student eligible for award of the final qualification?',
        "answer": 'A student must successfully complete all prescribed academic and evaluation requirements within the applicable programme duration/validity and satisfy the conditions laid down by the University.',
        "category": 'Credentials & Convocation'
    },
    {
        "keywords": ['degree diploma certificate issue', 'digilocker ignou', 'convocation credentials'],
        "question": 'How are degree/diploma/certificate credentials issued?',
        "answer": 'IGNOU issues academic credentials through its prescribed award and convocation processes. Digital credentials may also be made available through designated digital platforms such as DigiLocker, subject to the University\'s process.',
        "category": 'Credentials & Convocation'
    },
    {
        "keywords": ['obtain transcript ignou', 'official transcript process', 'transcript documentation fee'],
        "question": 'How can I obtain a transcript?',
        "answer": 'Apply through the designated transcript/verification procedure and comply with the prescribed application, documentation and fee requirements.',
        "category": 'Credentials & Convocation'
    },
    {
        "keywords": ['certificate error correction', 'degree correction request', 'name mistake certificate'],
        "question": 'What should I do if my certificate or degree has an error?',
        "answer": 'Submit a correction request through the competent University office with documentary evidence and follow the prescribed verification/correction procedure.',
        "category": 'Credentials & Convocation'
    },

    # --- 12. STUDENT GRIEVANCES & SUPPORT ---
    {
        "keywords": ['submit grievance ignou', 'igram portal', 'student grievance redressal'],
        "question": 'Where should I submit a grievance relating to my IGNOU student services?',
        "answer": 'Use the appropriate official grievance mechanism, such as iGRAM, or another portal/channel designated for the nature of the grievance. Keep the grievance specific, factual, and supported by relevant documents.',
        "category": 'Grievance & Support'
    },
    {
        "keywords": ['write effective grievance', 'grievance representation details', 'igram complaint guidelines'],
        "question": 'How should I write an effective grievance?',
        "answer": 'Clearly state your enrolment number, programme, course code (where relevant), the issue, chronology of events, action already taken, and the specific relief requested. Attach supporting documents wherever required.',
        "category": 'Grievance & Support'
    },
    {
        "keywords": ['multiple grievances same issue', 'duplicate igram tickets', 'repetitive complaints'],
        "question": 'Can I submit multiple grievances for the same issue?',
        "answer": 'Avoid submitting repetitive grievances without new information. A concise, evidence-based representation helps the concerned office examine and resolve the matter efficiently.',
        "category": 'Grievance & Support'
    },
    {
        "keywords": ['incorrect grievance response', 'appeal igram response', 'unresolved grievance'],
        "question": 'What if I receive an incorrect or incomplete response?',
        "answer": 'Review the response and, where necessary, submit a reasoned representation through the appropriate official channel, clearly identifying the unresolved point and providing documentary evidence.',
        "category": 'Grievance & Support'
    },

    # --- 13. GENERAL QUERIES & RESPONSIBILITIES ---
    {
        "keywords": ['difference study centre regional centre', 'rc vs sc', 'nodal office vs support centre'],
        "question": 'What is the difference between a Study Centre and a Regional Centre?',
        "answer": 'A Regional Centre is the nodal office for a region; several study centres under it provide support services like counselling and assignment submission.',
        "category": 'General'
    },
    {
        "keywords": ['update address phone number', 'change address ignou', 'contact details correction'],
        "question": 'How do I get my address or phone number updated?',
        "answer": 'Email your Regional Centre with a copy of your ID card, or submit a written request with the ID copy in person.',
        "category": 'General'
    },
    {
        "keywords": ['refund application fee', 'admission fee refund policy', 'fee adjustment'],
        "question": 'What is the rule regarding refund of application fee?',
        "answer": 'Once paid, the fee is not refunded under any circumstances, nor adjustable against another programme — except when the University itself denies admission, in which case the fee is refunded (minus registration fee) by the same payment method used by the applicant.',
        "category": 'General'
    },
    {
        "keywords": ['responsibilities ignou student', 'student duties deadlines', 'academic compliance'],
        "question": 'What are the most important responsibilities of an IGNOU student?',
        "answer": 'Maintain accurate personal details, complete re-registration on time, submit assignments and examination forms within deadlines, appear for eligible examinations, monitor official notifications, retain transaction/submission records, and comply with academic and examination rules.',
        "category": 'General'
    },
    {
        "keywords": ['social media information reliability', 'unofficial ignou websites', 'official ignou portal only'],
        "question": 'Should I rely on information shared on social media or unofficial websites?',
        "answer": 'No. Treat the official IGNOU website, official portals, Regional Centre notices and University notifications as the authoritative sources. Do not rely on unofficial information for deadlines, fees, eligibility or academic rules.',
        "category": 'General'
    },
    {
        "keywords": ['important records to retain', 'proof of submission receipt', 'fee receipts keeping'],
        "question": 'What records should I retain?',
        "answer": 'Admission confirmation, fee receipts, re-registration confirmation, assignment submission proof, examination-form receipt, hall ticket, grade card/result records, project approval/submission proof, and correspondence relating to any unresolved matter.',
        "category": 'General'
    },

    # --- 14. INTERNATIONAL STUDENTS ---
    {
        "keywords": ['international student admission', 'overseas partner institutes', 'study outside india'],
        "question": 'How can a student residing outside India take admission in IGNOU?',
        "answer": "Through IGNOU's overseas Partner Institutes — contact your nearest Partner Institute and submit the admission form with the prescribed fee.",
        "category": 'International Students'
    },
    {
        "keywords": ['admission without partner institute', 'no partner institute country'],
        "question": 'Can admission be taken from a place with no Partner Institute?',
        "answer": "No. Partner Institutes handle assignments, exams and other support, so a programme can't be offered where none exists.",
        "category": 'International Students'
    },
    {
        "keywords": ['international student exam fee', 'saarc non saarc fee structure'],
        "question": 'What is the examination fee structure for international students?',
        "answer": 'A two-tier structure — one rate for SAARC countries, another for non-SAARC. Exact figures are on the University website.',
        "category": 'International Students'
    },
    {
        "keywords": ['international student degree certificate', 'international division ignou maidan garhi'],
        "question": 'How is the international-student degree certificate obtained?',
        "answer": 'After completing all programme components, apply with the prescribed fee to the International Division, IGNOU, Maidan Garhi, New Delhi.',
        "category": 'International Students'
    },

    # --- 15. IMPORTANT WEBSITES & CONTACTS ---
    {
        "keywords": ['official website contact details', 'samarth portal link', 'egyankosh igram links', 'headquarters phone number'],
        "question": 'What are the important IGNOU websites and contact details?',
        "answer": 'Official website: www.ignou.ac.in | Admission: ignouadmission.samarth.edu.in (ODL), ignouiop.samarth.edu.in (Online) | Re-registration: onlinerr.ignou.ac.in | Study material: www.egyankosh.ac.in | Assignments: ignou.ac.in/studentService/download/assignments | Exams: exam.ignou.ac.in | Grievances: igram.ignou.ac.in | HQ: IGNOU, Maidan Garhi, New Delhi – 110068 (Phone: 29572513, 29572514).',
        "category": 'Contacts & Portals'
    }
]

# Initialize structured FAQs array
FAQS = []
for idx, entry in enumerate(RAW_FAQS, start=1):
    FAQS.append({
        "id": idx,
        "category": entry["category"],
        "question": entry["question"],
        "answer": entry["answer"],
        "keywords": entry["keywords"],
        "aliases": [],
        "source": "IGNOU FAQ Official Document"
    })

# ==========================================
# 3. SEARCH, SUGGESTION & SCORING LOGIC
# ==========================================
def normalize_text(text):
    """Lowercases text and removes punctuation for matching."""
    return re.sub(r'[^a-z0-9\s]', '', str(text).lower()).strip()

def get_suggestions(user_query, top_n=3, exclude_id=None):
    """
    Finds top matching question suggestions based on word overlaps and fuzzy similarity.
    """
    norm_query = normalize_text(user_query)
    stop_words = {"is", "a", "the", "in", "to", "for", "of", "and", "or", "me", "kaise", "kyu", "kya", "hai", "sir", "kab", "tak", "how", "what", "where", "can"}
    query_words = set(norm_query.split()) - stop_words
    
    scored_suggestions = []

    for faq in FAQS:
        if exclude_id and faq["id"] == exclude_id:
            continue

        question_norm = normalize_text(faq["question"])
        kw_norm = [normalize_text(kw) for kw in faq["keywords"]]
        
        q_word_matches = sum(1 for word in query_words if word in question_norm)
        kw_word_matches = sum(1 for word in query_words if any(word in kw for kw in kw_norm))
        
        fuzzy_score = fuzz.token_set_ratio(norm_query, question_norm) / 100.0

        total_suggestion_score = (q_word_matches * 0.4) + (kw_word_matches * 0.4) + (fuzzy_score * 0.2)

        if total_suggestion_score > 0.15:
            scored_suggestions.append({
                "faq_id": faq["id"],
                "question": faq["question"],
                "category": faq["category"],
                "score": round(total_suggestion_score, 2)
            })

    scored_suggestions.sort(key=lambda x: x["score"], reverse=True)
    return scored_suggestions[:top_n]

def search_faq(user_query):
    """Implements lightweight scoring using RapidFuzz ratio matching and keyword hit scoring."""
    english_query = translate_to_english(user_query)
    norm_query = normalize_text(english_query)
    
    best_faq = None
    max_score = 0.0

    for faq in FAQS:
        q_score = fuzz.token_set_ratio(norm_query, normalize_text(faq['question'])) / 100.0
        kw_hits = sum(1 for kw in faq['keywords'] if normalize_text(kw) in norm_query)
        kw_score = min(1.0, kw_hits * 0.3)
        
        combined_score = (q_score * 0.6) + (kw_score * 0.4)
        
        if combined_score > max_score:
            max_score = combined_score
            best_faq = faq
            
    return best_faq, max_score

# ==========================================
# 4. API ENDPOINTS
# ==========================================
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok", 
        "service": "IGNOU Student FAQ Chatbot", 
        "total_faqs": len(FAQS)
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    if not data or "query" not in data:
        return jsonify({
            "success": False,
            "answer": "Please provide a valid query.",
            "category": "Error",
            "confidence": 0.0,
            "faq_id": None,
            "suggestions": []
        }), 400
        
    user_query = data["query"]
    best_faq, confidence = search_faq(user_query)
    
    time_sensitive_keywords = ['date', 'deadline', 'last date', 'fee', 'schedule', 'notification', 'fees']
    needs_disclaimer = any(ts in user_query.lower() for ts in time_sensitive_keywords)

    if confidence >= 0.75:
        ans = best_faq['answer']
        if needs_disclaimer:
            ans += "\n\n*Note: Please verify the latest notification issued by IGNOU before taking action.*"
            
        suggestions = get_suggestions(user_query, exclude_id=best_faq['id'])
        return jsonify({
            "success": True,
            "answer": ans,
            "category": best_faq['category'],
            "confidence": round(confidence, 2),
            "faq_id": best_faq['id'],
            "suggestions": suggestions
        })
        
    elif confidence >= 0.45:
        ans = "Based on the available IGNOU FAQ information...\n\n" + best_faq['answer']
        if needs_disclaimer:
            ans += "\n\n*Note: Please verify the latest notification issued by IGNOU before taking action.*"
            
        suggestions = get_suggestions(user_query, exclude_id=best_faq['id'])
        return jsonify({
            "success": True,
            "answer": ans,
            "category": best_faq['category'],
            "confidence": round(confidence, 2),
            "faq_id": best_faq['id'],
            "suggestions": suggestions
        })
        
    else:
        suggestions = get_suggestions(user_query)
        return jsonify({
            "success": False,
            "answer": "I could not find a reliable answer to this specific query. Here are some related questions you might want to ask:",
            "category": "General",
            "confidence": round(confidence, 2),
            "faq_id": None,
            "suggestions": suggestions
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)