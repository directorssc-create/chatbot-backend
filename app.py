import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Google Sites

# Your IGNOU FAQs stored safely inside the code
# Auto-generated from ignou_faqs_xlsx.xlsx -- 420 FAQs across 16 categories
FAQS = [
    {
        "keywords": ['new admission', 'ignou admission process', 'apply online', 'admission form', 'registration'],
        "question": 'Sir, mujhe IGNOU me naya admission lena hai. Admission kaise karu?',
        "answer": 'IGNOU admission process is conducted through the official admission portal. Students need to register online, select the desired programme, fill the application form, upload required documents, pay the prescribed fee and submit the application. Students should check the latest admission notification before applying.'
    },
    {
        "keywords": ['ignou registration', 'create account', 'new user registration'],
        "question": 'Mera IGNOU registration kaise hoga?',
        "answer": 'Registration is the first step for applying to an IGNOU programme. Students must create an account on the admission portal using a valid mobile number and email ID.'
    },
    {
        "keywords": ['ignou eligibility', 'programme qualification', 'admission criteria'],
        "question": 'Mera admission eligibility clear nahi hai. Main kaunsa programme le sakta hu?',
        "answer": 'Programme eligibility varies according to the programme. Students should check the official programme guide and eligibility criteria before applying.'
    },
    {
        "keywords": ['programme change', 'wrong course selection', 'change programme'],
        "question": 'Maine galat programme select kar liya hai. Kya programme change ho sakta hai?',
        "answer": 'Programme change after admission is allowed only according to IGNOU rules and within the prescribed period, if applicable. Students should submit a request through the prescribed process.'
    },
    {
        "keywords": ['wrong programme', 'admission correction', 'course correction'],
        "question": 'Maine wrong programme choose kar diya hai. Kya correction possible hai?',
        "answer": 'Students should immediately contact IGNOU through the appropriate channel if incorrect programme selection has been made. Correction depends on the admission status and applicable rules.'
    },
    {
        "keywords": ['regional centre selection', 'rc choice', 'learner support centre'],
        "question": 'Regional Centre ka selection kaise karna hai?',
        "answer": 'Students should select the Regional Centre based on their location and programme availability. Regional Centre provides learner support services.'
    },
    {
        "keywords": ['study centre selection', 'centre allotment', 'counselling centre'],
        "question": 'Study Centre ka selection kaise hota hai?',
        "answer": 'Study Centre allocation depends on programme availability, learner location and IGNOU norms. The selected Study Centre may be allotted after admission processing.'
    },
    {
        "keywords": ['admission portal error', 'website not opening', 'technical problem'],
        "question": 'Mera admission portal open nahi ho raha hai. Kya karu?',
        "answer": 'Portal issues may occur due to technical problems, browser settings or heavy traffic. Students should retry after basic troubleshooting.'
    },
    {
        "keywords": ['form submission problem', 'application pending', 'admission error'],
        "question": 'Maine admission form fill kar diya hai lekin submit nahi ho raha hai.',
        "answer": 'If the application is not submitted, students should verify mandatory fields, uploaded documents and payment requirements before final submission.'
    },
    {
        "keywords": ['fee payment', 'admission fee', 'payment receipt', 'online payment'],
        "question": 'Admission fee payment kaise karni hai?',
        "answer": 'Admission fee can be paid through available online payment options provided on the official admission portal. Students should save the payment receipt after successful payment.'
    },
    {
        "keywords": ['fee deducted', 'payment successful but admission pending', 'transaction issue', 'admission confirmation'],
        "question": 'Maine fees pay kar di hai lekin admission confirm nahi ho raha hai. Kya karu?',
        "answer": 'If the admission fee has been deducted but admission confirmation is not visible, students should wait for payment verification and check the admission portal status. In case of continued delay, submit the payment details through the official support mechanism.'
    },
    {
        "keywords": ['payment failure', 'money deducted', 'refund', 'failed transaction'],
        "question": 'Payment fail ho gaya hai lekin paisa account se kat gaya hai. Refund kab milega?',
        "answer": 'In case of failed transactions where money is deducted, the amount is normally processed according to banking/payment gateway reconciliation rules. Students should retain transaction proof and avoid making repeated payments immediately.'
    },
    {
        "keywords": ['fee refund', 'admission cancellation refund', 'refund status'],
        "question": 'Admission fee refund ka process kya hai?',
        "answer": 'Refund of fees is governed by IGNOU admission cancellation and refund rules applicable to the specific admission cycle. Students should check the latest refund notification before submitting a request.'
    },
    {
        "keywords": ['admission cancellation', 'cancel admission', 'withdrawal request'],
        "question": 'Kya main apna IGNOU admission cancel kar sakta hu?',
        "answer": 'Admission cancellation may be permitted according to IGNOU rules and within the specified period. Students should submit a request through the prescribed procedure.'
    },
    {
        "keywords": ['re-registration', 'semester continuation', 'yearly registration'],
        "question": 'Mera re-registration kaise hoga?',
        "answer": 'Existing IGNOU students who wish to continue their programme must complete re-registration through the official portal during the notified period.'
    },
    {
        "keywords": ['late re-registration', 'missed deadline', 'registration extension'],
        "question": 'Re-registration ki last date miss ho gayi hai. Kya kar sakta hu?',
        "answer": 'Re-registration windows and late fee provisions, if any, are announced through official notifications. Students should check the latest updates and apply within the available period.'
    },
    {
        "keywords": ['abc id', 'academic bank of credits', 'credit storage', 'digilocker'],
        "question": 'IGNOU admission ke liye ABC ID kya hota hai?',
        "answer": 'Academic Bank of Credits (ABC) ID is used for maintaining academic credits digitally as per applicable academic frameworks. Students may need to provide their ABC ID during admission or academic processes wherever notified.'
    },
    {
        "keywords": ['abc id problem', 'unable to create abc account', 'identity mismatch'],
        "question": 'ABC ID nahi ban rahi hai. Kya karu?',
        "answer": 'Students facing difficulty creating ABC ID should verify their identity details and follow the support process provided by the ABC platform.'
    },
    {
        "keywords": ['deb id', 'distance education id', 'odl admission', 'ugc deb'],
        "question": 'DEB ID kya hai aur kaise banani hai?',
        "answer": 'DEB ID is required for learners enrolling in certain Open and Distance Learning programmes as per applicable regulations. Students should create and verify their DEB ID before completing admission wherever required.'
    },
    {
        "keywords": ['identity verification', 'document mismatch', 'admission verification problem'],
        "question": 'Admission ke time identity verification problem aa rahi hai. Kya karu?',
        "answer": 'Identity verification issues may occur due to mismatch in personal details, unclear documents or technical problems. Students should verify details and upload valid documents again if permitted.'
    },
    {
        "keywords": ['document upload error', 'file upload problem', 'admission documents'],
        "question": 'Mera document upload nahi ho raha hai. Kya karu?',
        "answer": 'Document upload issues may occur due to incorrect file size, format, internet connectivity or technical problems. Students should upload documents according to the instructions provided on the admission portal.'
    },
    {
        "keywords": ['photo upload', 'signature upload', 'image error'],
        "question": 'Photo aur signature upload nahi ho raha hai.',
        "answer": 'Photograph and signature must be uploaded in the prescribed format and size mentioned in the admission guidelines.'
    },
    {
        "keywords": ['wrong document uploaded', 'document correction', 'admission correction'],
        "question": 'Maine galat document upload kar diya hai. Kya correction possible hai?',
        "answer": 'Correction facility depends on the admission portal rules and correction window provided by IGNOU. Students should check available correction options.'
    },
    {
        "keywords": ['category certificate', 'sc st obc certificate', 'document pending'],
        "question": 'Category certificate upload nahi hua hai. Kya admission cancel ho jayega?',
        "answer": 'Students should submit valid category certificates wherever required. Missing documents may affect benefit eligibility or verification. Students should follow official instructions for document submission.'
    },
    {
        "keywords": ['admission pending', 'verification pending', 'status not updated'],
        "question": 'Mera admission status abhi bhi pending dikha raha hai.',
        "answer": 'Admission status may remain pending until application verification, fee confirmation and document checking are completed. Students should regularly check the admission portal.'
    },
    {
        "keywords": ['enrollment number', 'admission confirmation', 'registration number'],
        "question": 'Admission confirm hone ke baad enrollment number kab milega?',
        "answer": 'Enrollment number is generated after successful processing of admission. Students should check their admission portal and registered email/SMS notifications.'
    },
    {
        "keywords": ['admission receipt', 'confirmation letter', 'fee receipt'],
        "question": 'Mujhe admission confirmation receipt nahi mil rahi hai.',
        "answer": 'Students should download the confirmation receipt from the admission portal after successful admission processing.'
    },
    {
        "keywords": ['duplicate application', 'multiple forms', 'duplicate admission'],
        "question": 'Maine do baar admission form submit kar diya hai. Kya hoga?',
        "answer": 'Multiple applications may create duplication issues. Students should inform IGNOU through the appropriate channel and provide application details for verification.'
    },
    {
        "keywords": ['login problem', 'admission portal login', 'forgot password'],
        "question": 'Maine registration kar liya hai lekin login nahi ho raha hai.',
        "answer": 'Login problems may occur due to incorrect credentials, browser issues or temporary technical problems. Students should use the password recovery option.'
    },
    {
        "keywords": ['programme unavailable', 'course not showing', 'admission programme list'],
        "question": 'Jo programme mujhe chahiye woh admission portal par nahi dikh raha hai.',
        "answer": 'Programme availability depends on admission cycle, region, eligibility and programme offering status. Students should check the current admission notification.'
    },
    {
        "keywords": ['eligibility check', 'qualification verification', 'admission criteria'],
        "question": 'Mera qualification IGNOU programme ke liye valid hai ya nahi?',
        "answer": 'IGNOU programme eligibility is decided according to the prescribed eligibility criteria mentioned in the programme details. Students should verify their qualification before applying.'
    },
    {
        "keywords": ['low marks', 'percentage requirement', 'admission eligibility'],
        "question": 'Mere marks eligibility se kam hain. Kya admission mil sakta hai?',
        "answer": 'Admission eligibility depends on the rules of the specific programme. Some programmes may have minimum percentage requirements while others may not. Students should refer to the official programme guide.'
    },
    {
        "keywords": ['admission last date', 'admission extension', 'late admission'],
        "question": 'Admission ki last date nikal gayi hai. Kya ab admission ho sakta hai?',
        "answer": 'Admission dates are announced for each admission cycle. Extension, if any, is notified officially. Students should check the latest admission announcements.'
    },
    {
        "keywords": ['late fee admission', 'delayed admission', 'admission extension'],
        "question": 'Kya late fee ke saath admission ho sakta hai?',
        "answer": 'Late admission facility depends on IGNOU policy and the admission cycle. Students should check official notifications for availability of late submission options.'
    },
    {
        "keywords": ['online admission', 'digital admission', 'apply online'],
        "question": 'IGNOU me online admission kaise hota hai?',
        "answer": 'IGNOU provides online admission facilities through its official admission portal. Students can complete registration, application submission and fee payment online.'
    },
    {
        "keywords": ['offline admission', 'admission centre', 'application process'],
        "question": 'Kya IGNOU me offline admission bhi hota hai?',
        "answer": 'Admission process is generally conducted through the prescribed online mode. Students should follow the latest admission notification for available procedures.'
    },
    {
        "keywords": ['working professional', 'job holder admission', 'flexible learning'],
        "question": 'Main working professional hu. Kya IGNOU me admission le sakta hu?',
        "answer": 'IGNOU programmes are designed to support learners including working professionals. Students should select programmes according to eligibility and personal study requirements.'
    },
    {
        "keywords": ['defence admission', 'army personnel', 'military learner'],
        "question": 'Defence personnel ke liye IGNOU admission ka process kya hai?',
        "answer": 'Defence personnel can apply for eligible IGNOU programmes through the regular admission process. Special facilities may be available according to applicable government/IGNOU provisions.'
    },
    {
        "keywords": ['foreign student admission', 'international learner', 'overseas admission'],
        "question": 'Foreign student IGNOU me admission kaise le sakta hai?',
        "answer": 'International learners should follow the admission procedure applicable to foreign nationals. They should verify programme availability, eligibility and fee requirements before applying.'
    },
    {
        "keywords": ['foreign qualification', 'degree equivalence', 'overseas certificate'],
        "question": 'Meri foreign degree hai. Kya IGNOU admission ke liye valid hogi?',
        "answer": 'Foreign qualifications are considered according to applicable recognition and verification requirements. Students should provide necessary documents for evaluation.'
    },
    {
        "keywords": ['jail inmate admission', 'prison education', 'special learner'],
        "question": 'Jail me rehne wale students IGNOU me admission kaise le sakte hain?',
        "answer": 'IGNOU provides educational opportunities for eligible learners in correctional institutions through approved channels. Admission is processed according to IGNOU guidelines and coordination with concerned authorities.'
    },
    {
        "keywords": ['rural learner', 'village student', 'distance education support'],
        "question": 'Rural area me rehne wale students IGNOU admission kaise le sakte hain?',
        "answer": 'IGNOU supports learners across India through its Regional Centres and Study Centres. Rural learners can apply through the online admission system and access learner support services.'
    },
    {
        "keywords": ['senior citizen admission', 'elderly learner', 'flexible education'],
        "question": 'Senior citizen ke liye IGNOU me admission available hai?',
        "answer": 'Senior citizens can apply for eligible IGNOU programmes if they fulfil the programme eligibility criteria. IGNOU provides flexible learning opportunities for learners of all age groups.'
    },
    {
        "keywords": ['divyang admission', 'disability support', 'accessible education'],
        "question": 'Divyang student ke liye admission me kya facility hai?',
        "answer": 'IGNOU supports inclusive education and provides facilities for Divyang learners according to applicable guidelines. Students should mention relevant requirements during admission.'
    },
    {
        "keywords": ['document verification pending', 'admission verification', 'approval delay'],
        "question": 'Admission me document verification complete nahi ho raha hai.',
        "answer": 'Document verification may take time due to application volume, document mismatch or incomplete information. Students should check portal remarks and respond accordingly.'
    },
    {
        "keywords": ['admission correction', 'edit application', 'correction window'],
        "question": 'Admission form me correction kab aur kaise kar sakte hain?',
        "answer": 'IGNOU may provide correction facilities during notified correction windows. Students should use only official correction mechanisms.'
    },
    {
        "keywords": ['name correction', 'spelling mistake', 'personal details update'],
        "question": 'Mere naam me spelling mistake hai. Admission form me kaise correct karu?',
        "answer": 'Name correction depends on the stage of admission processing and applicable rules. Students should submit a request with supporting documents.'
    },
    {
        "keywords": ['dob correction', 'birth date update', 'admission details'],
        "question": 'Date of Birth galat fill ho gayi hai. Kya change ho sakti hai?',
        "answer": 'Date of Birth correction requires verification and supporting documents. Students should submit a request through the prescribed procedure.'
    },
    {
        "keywords": ['application withdrawal', 'cancel application', 'admission request removal'],
        "question": 'Maine admission application submit kar di hai, kya use withdraw kar sakta hu?',
        "answer": 'Withdrawal of application depends on the status of processing and applicable admission rules. Students should contact the concerned authority if withdrawal is required.'
    },
    {
        "keywords": ['final admission status', 'admission confirmation', 'enrollment generated'],
        "question": 'Kaise pata chalega ki mera IGNOU admission final confirm ho gaya hai?',
        "answer": 'Admission is considered confirmed after successful processing, verification and generation of admission confirmation/enrollment details. Students should regularly check the official portal.'
    },
    {
        "keywords": ['login problem', 'unable to login', 'student portal issue', 'account access'],
        "question": 'Mera IGNOU login nahi ho raha hai. Kya karu?',
        "answer": 'Students should verify their username, password and registered details before attempting login. Login issues may occur due to incorrect credentials, account lock, browser issues or temporary technical problems.'
    },
    {
        "keywords": ['forgot username', 'lost enrollment number', 'login id recovery'],
        "question": 'Mera username ya enrollment number yaad nahi hai. Kaise milega?',
        "answer": 'Students can retrieve their login details through available recovery options or by checking admission-related communications.'
    },
    {
        "keywords": ['forgot password', 'reset password', 'login recovery'],
        "question": 'Mera password bhool gaya hu. Password reset kaise karu?',
        "answer": 'Students can reset their password through the official password recovery facility using registered contact details.'
    },
    {
        "keywords": ['otp not received', 'password reset issue', 'verification problem'],
        "question": 'Password reset OTP nahi aa raha hai. Kya karu?',
        "answer": 'OTP delivery may be delayed due to network issues, incorrect registered details or technical problems. Students should verify their contact information.'
    },
    {
        "keywords": ['change mobile number', 'update phone number', 'profile correction'],
        "question": 'Mera mobile number change ho gaya hai. IGNOU record me update kaise karu?',
        "answer": 'Students should update their mobile number through the permitted profile update facility or submit a request through the appropriate channel.'
    },
    {
        "keywords": ['email change', 'update email id', 'profile update'],
        "question": 'Mera email ID change ho gaya hai. Kaise update karu?',
        "answer": 'Students should ensure their email ID is updated because important academic communications are sent through registered contact details.'
    },
    {
        "keywords": ['name correction', 'profile mistake', 'personal details correction'],
        "question": 'Mere profile me naam galat show ho raha hai. Correction kaise hogi?',
        "answer": 'Name correction requires verification and supporting documents. Students should submit correction requests through the prescribed process.'
    },
    {
        "keywords": ['address update', 'change address', 'communication details'],
        "question": 'Mera address change ho gaya hai. IGNOU me update kaise karu?',
        "answer": 'Students should update their communication address to receive academic services and correspondence without delay.'
    },
    {
        "keywords": ['enrollment issue', 'enrollment number error', 'student record'],
        "question": 'Mera enrollment number kaam nahi kar raha hai.',
        "answer": 'Enrollment number issues may occur due to incorrect entry, account synchronization delay or technical problems.'
    },
    {
        "keywords": ['profile update', 'personal information correction', 'portal issue'],
        "question": 'Student portal par meri personal details update nahi ho rahi hain.',
        "answer": 'Profile updates depend on available correction facilities and applicable IGNOU procedures. Students should use official channels for changes not available online.'
    },
    {
        "keywords": ['account locked', 'login blocked', 'unlock account'],
        "question": 'Mera student account lock ho gaya hai. Kaise unlock karu?',
        "answer": 'Student accounts may get locked due to repeated incorrect login attempts or security reasons. Students should use account recovery options or contact portal support.'
    },
    {
        "keywords": ['duplicate login', 'multiple accounts', 'user id issue'],
        "question": 'Mere naam se do login ID ban gayi hain. Kya karu?',
        "answer": 'Students should use only one valid account linked with their admission record. Duplicate accounts should be reported for verification and correction.'
    },
    {
        "keywords": ['parent name correction', 'personal details update', 'profile correction'],
        "question": "Mere profile me father's/mother's name galat hai. Correction kaise hogi?",
        "answer": 'Correction of personal information requires verification through prescribed procedures and supporting documents.'
    },
    {
        "keywords": ['dob update', 'date of birth correction', 'student record'],
        "question": 'Meri date of birth profile me galat hai. Kaise change karu?',
        "answer": 'Date of Birth correction requires valid proof and approval from the concerned authority. Students should submit a formal correction request.'
    },
    {
        "keywords": ['gender correction', 'profile details', 'student information'],
        "question": 'Mera gender profile me galat show ho raha hai. Correction kaise hogi?',
        "answer": 'Students can request correction of gender details by providing appropriate supporting documents through the official process.'
    },
    {
        "keywords": ['category correction', 'caste certificate update', 'profile change'],
        "question": 'Mera category details galat update ho gaya hai. Kya correction possible hai?',
        "answer": 'Category information correction is processed according to IGNOU rules and requires supporting documents.'
    },
    {
        "keywords": ['guardian update', 'family details', 'profile correction'],
        "question": 'Guardian details update karni hai. Kaise karu?',
        "answer": 'Guardian details can be updated through available profile correction facilities or by submitting a request through the appropriate channel.'
    },
    {
        "keywords": ['auto logout', 'session expired', 'portal problem'],
        "question": 'Student portal baar-baar logout ho raha hai. Kya problem hai?',
        "answer": 'Automatic logout may occur due to session timeout, browser settings, internet instability or security measures.'
    },
    {
        "keywords": ['mobile login issue', 'portal not opening', 'technical error'],
        "question": 'IGNOU portal mobile me open nahi ho raha hai. Kya karu?',
        "answer": 'Students should use a compatible browser and stable internet connection. Some portal features may work better on updated desktop/mobile browsers.'
    },
    {
        "keywords": ['ignou app login', 'mobile application problem', 'app error'],
        "question": 'IGNOU mobile app me login nahi ho raha hai.',
        "answer": 'App login issues may occur due to incorrect credentials, outdated application version or connectivity problems.'
    },
    {
        "keywords": ['portal error', 'website issue', 'technical problem', 'system error'],
        "question": 'IGNOU portal par technical error aa raha hai. Kya karu?',
        "answer": 'Technical errors may occur due to server maintenance, heavy traffic, browser issues or temporary system problems. Students should try basic troubleshooting before reporting the issue.'
    },
    {
        "keywords": ['wrong programme code', 'course mismatch', 'admission record correction'],
        "question": 'Mere profile me programme code galat show ho raha hai.',
        "answer": 'Programme details displayed in the student profile are based on admission records. Any mismatch should be reported for verification and correction.'
    },
    {
        "keywords": ['enrollment mismatch', 'programme mismatch', 'student record error'],
        "question": 'Mere enrollment number aur programme details match nahi kar rahe hain.',
        "answer": 'A mismatch between enrollment number records and programme details requires verification by the concerned division. Students should not create a new account or submit duplicate requests.'
    },
    {
        "keywords": ['profile not updated', 'data synchronization', 'update pending'],
        "question": 'Mera profile update ho gaya hai lekin portal par reflect nahi ho raha hai.',
        "answer": 'Profile updates may require processing time before appearing across all IGNOU systems. Students should wait for synchronization and verify again.'
    },
    {
        "keywords": ['student record verification', 'profile check', 'personal details'],
        "question": 'Apne IGNOU student record ki final verification kaise karu?',
        "answer": 'Students should verify their personal details, programme information, contact details and academic records regularly through official IGNOU systems.'
    },
    {
        "keywords": ['study material', 'books delivery', 'ignou books', 'printed material'],
        "question": 'IGNOU ka study material kab milega?',
        "answer": 'IGNOU dispatches printed study material to eligible learners after admission confirmation and completion of required processing. Dispatch timelines may vary depending on programme, availability and operational conditions. Students should also use digital resources available through official platforms.'
    },
    {
        "keywords": ['books not received', 'study material pending', 'material delivery'],
        "question": 'Mera admission confirm ho gaya hai lekin books nahi mili hain. Kya karu?',
        "answer": 'Students should first verify dispatch status and ensure that the correct communication address is available in IGNOU records.'
    },
    {
        "keywords": ['material tracking', 'book status', 'dispatch status'],
        "question": 'Study material ka status kaise check kar sakta hu?',
        "answer": 'Students can check study material related updates through available IGNOU services and contact the concerned Regional Centre or support section if required.'
    },
    {
        "keywords": ['wrong address', 'book delivery problem', 'address correction'],
        "question": 'Mera study material wrong address par chala gaya hai.',
        "answer": 'Study material is dispatched according to the address available in IGNOU records. Students should ensure their communication address is updated and report incorrect delivery details.'
    },
    {
        "keywords": ['missing books', 'incomplete material', 'course book missing'],
        "question": 'Mujhe kuch books mili hain lekin kuch missing hain.',
        "answer": 'Students should report missing books by providing programme and course details. Missing material requests are processed according to availability and distribution procedures.'
    },
    {
        "keywords": ['wrong books', 'incorrect material', 'replacement request'],
        "question": 'Galat programme ki books mil gayi hain. Kya karu?',
        "answer": 'Students who receive incorrect study material should report the issue with complete programme and course details for verification and replacement guidance.'
    },
    {
        "keywords": ['damaged books', 'book replacement', 'material complaint'],
        "question": 'Study material kharab condition me mila hai. Replacement kaise hoga?',
        "answer": 'Damaged study material cases should be reported with relevant details. Replacement depends on verification and availability of material.'
    },
    {
        "keywords": ['digital material', 'online books', 'egyankosh', 'pdf books'],
        "question": 'Kya IGNOU ka digital study material online mil sakta hai?',
        "answer": 'IGNOU provides digital learning resources through official platforms. Students can access digital materials using programme and course details.'
    },
    {
        "keywords": ['egyankosh problem', 'pdf not available', 'digital books'],
        "question": 'eGyanKosh par material nahi mil raha hai. Kya karu?',
        "answer": 'Students should verify course codes and search details while accessing digital resources. Some materials may be updated according to programme schedules.'
    },
    {
        "keywords": ['printed books', 'digital material', 'study resources'],
        "question": 'Kya printed books aur digital material dono milte hain?',
        "answer": 'IGNOU provides study support through printed material and digital resources. Availability depends on programme guidelines and applicable policies.'
    },
    {
        "keywords": ['material delayed', 'books pending', 'study material not received'],
        "question": 'Admission ke bahut din baad bhi study material nahi mila hai. Kya karu?',
        "answer": 'If study material is not received within the expected period after admission confirmation, students should verify their dispatch status, address details and programme material availability.'
    },
    {
        "keywords": ['foreign student books', 'overseas material delivery', 'international learner'],
        "question": 'International student ko IGNOU books kaise milengi?',
        "answer": 'International students receive study material according to the applicable international learner procedures and programme arrangements. Students should verify delivery arrangements during admission.'
    },
    {
        "keywords": ['collect books', 'rc material', 'study centre books'],
        "question": 'Kya main Regional Centre se study material le sakta hu?',
        "answer": 'Availability of study material at Regional Centres depends on programme, stock and applicable arrangements. Students should contact their Regional Centre before visiting.'
    },
    {
        "keywords": ['online programme material', 'lms content', 'digital books'],
        "question": 'Online programme students ko study material kaise milega?',
        "answer": 'Online programme learners generally access learning resources through digital platforms. Availability of printed material depends on programme guidelines.'
    },
    {
        "keywords": ['extra books', 'additional material', 'course material request'],
        "question": 'Mujhe extra study material ya additional books chahiye. Kya mil sakti hain?',
        "answer": 'Additional material availability depends on stock and applicable procedures. Students should contact the concerned section for guidance.'
    },
    {
        "keywords": ['material list', 'course books list', 'programme guide'],
        "question": 'Programme ke study material ki list kaise milegi?',
        "answer": 'Students can refer to programme details and course structure information to know the prescribed study material requirements.'
    },
    {
        "keywords": ['pdf download problem', 'ebook issue', 'digital content'],
        "question": 'eBooks ya PDF material download nahi ho raha hai.',
        "answer": 'Digital material access issues may occur due to internet problems, browser issues or platform maintenance. Students should try basic troubleshooting.'
    },
    {
        "keywords": ['mobile study material', 'online books', 'ignou app'],
        "question": 'Mobile phone se IGNOU study material kaise access karu?',
        "answer": 'Students can access available digital learning resources through compatible mobile browsers or official learning platforms.'
    },
    {
        "keywords": ['hindi books', 'language material', 'medium change'],
        "question": 'Mujhe Hindi medium material chahiye. Kya available hai?',
        "answer": 'Study material language availability depends on the programme structure and approved resources. Students should check programme details for available language options.'
    },
    {
        "keywords": ['regional centre contact', 'material support', 'learner support'],
        "question": 'Study material ke liye Regional Centre se kaise contact karu?',
        "answer": 'Students should contact their allotted Regional Centre for local learner support related to study material and delivery issues.'
    },
    {
        "keywords": ['jail student books', 'prison education material', 'special learner support'],
        "question": 'Jail me padhne wale students ko IGNOU study material kaise milega?',
        "answer": 'IGNOU provides learning support to eligible learners in correctional institutions through approved channels. Study material distribution is coordinated through authorized centres and concerned authorities.'
    },
    {
        "keywords": ['divyang material', 'accessible books', 'disability support'],
        "question": 'Divyang students ke liye accessible study material available hai kya?',
        "answer": 'IGNOU supports inclusive education. Accessibility support and alternative learning resources are provided according to applicable guidelines and availability.'
    },
    {
        "keywords": ['defence learner material', 'army student books', 'service personnel'],
        "question": 'Defence personnel ke liye study material delivery kaise hoti hai?',
        "answer": 'Defence personnel enrolled with IGNOU receive study support according to normal programme procedures and applicable arrangements with concerned centres.'
    },
    {
        "keywords": ['lost books', 'duplicate material', 'replacement books'],
        "question": 'Meri IGNOU books kho gayi hain. Kya dobara mil sakti hain?',
        "answer": 'Replacement of lost study material depends on availability and applicable procedures. Students may need to arrange replacement according to IGNOU guidelines.'
    },
    {
        "keywords": ['material complaint', 'unresolved books issue', 'escalation'],
        "question": 'Study material ki complaint ka final solution kaise milega?',
        "answer": 'Students should first contact the concerned Regional Centre/material support section. If the issue remains unresolved, they may escalate through official grievance channels.'
    },
    {
        "keywords": ['assignment download', 'assignment question paper', 'ignou assignment pdf'],
        "question": 'IGNOU assignment kahan se download kar sakte hain?',
        "answer": 'IGNOU assignments are made available through official IGNOU platforms. Students should download the latest assignment questions applicable to their programme and session.'
    },
    {
        "keywords": ['assignment not downloading', 'pdf problem', 'assignment error'],
        "question": 'Mera assignment download nahi ho raha hai. Kya karu?',
        "answer": 'Assignment download issues may occur due to internet problems, browser issues or temporary website traffic. Students should try accessing the official platform again.'
    },
    {
        "keywords": ['correct assignment', 'assignment session', 'valid assignment'],
        "question": 'Kaunsa assignment submit karna hai? Purana ya naya?',
        "answer": 'Students must submit the assignment applicable to their admission session and the current validity period announced by IGNOU.'
    },
    {
        "keywords": ['assignment format', 'assignment writing', 'submission format'],
        "question": 'Assignment banane ka format kya hai?',
        "answer": 'Students should prepare assignments according to IGNOU guidelines mentioned in the assignment booklet, including required information and presentation format.'
    },
    {
        "keywords": ['handwritten assignment', 'typed assignment', 'assignment rules'],
        "question": 'Assignment handwritten hona chahiye ya typed?',
        "answer": 'Assignment format depends on the instructions provided for the programme and submission method. Students should follow the latest guidelines issued by IGNOU.'
    },
    {
        "keywords": ['assignment last date', 'deadline', 'submission date'],
        "question": 'Assignment submit karne ki last date kya hai?',
        "answer": 'Assignment submission deadlines are notified by IGNOU from time to time. Students should check the latest official notification for applicable dates.'
    },
    {
        "keywords": ['late assignment', 'missed deadline', 'assignment extension'],
        "question": 'Assignment late submit kar sakte hain kya?',
        "answer": 'Late submission depends on IGNOU rules and the applicable submission schedule. Students should check official updates before submitting late assignments.'
    },
    {
        "keywords": ['assignment submission centre', 'submit assignment', 'study centre'],
        "question": 'Assignment kahan submit karna hai?',
        "answer": 'Assignment submission is generally made to the designated Study Centre/Regional Centre or through the prescribed online submission system wherever applicable.'
    },
    {
        "keywords": ['online assignment', 'digital submission', 'upload assignment'],
        "question": 'Kya assignment online submit kar sakte hain?',
        "answer": 'Online assignment submission facility depends on programme and instructions issued by IGNOU. Students should follow the notified submission process.'
    },
    {
        "keywords": ['assignment receipt', 'acknowledgement', 'submission proof'],
        "question": 'Assignment submit karne ke baad receipt kaise milegi?',
        "answer": 'Students should obtain acknowledgement from the submission centre or retain online submission confirmation as proof of submission.'
    },
    {
        "keywords": ['assignment status pending', 'marks not updated', 'submission update'],
        "question": 'Maine assignment submit kar diya hai lekin status update nahi hua. Kya karu?',
        "answer": 'Assignment status updates require evaluation and data entry by the concerned centre. Students should allow reasonable processing time and verify status through official systems.'
    },
    {
        "keywords": ['assignment marks missing', 'grade card update', 'marks not reflected'],
        "question": 'Assignment ke marks grade card me nahi aa rahe hain.',
        "answer": 'Assignment marks are updated after evaluation and processing by the concerned authorities. Delay may occur due to evaluation or data entry processes.'
    },
    {
        "keywords": ['assignment evaluation delay', 'pending evaluation'],
        "question": 'Assignment evaluation me bahut delay ho raha hai. Kya karu?',
        "answer": 'Assignment evaluation timelines depend on submission volume, evaluator availability and processing requirements. Students should track updates through official channels.'
    },
    {
        "keywords": ['wrong assignment marks', 'marks correction', 'evaluation complaint'],
        "question": 'Mere assignment marks galat aaye hain. Correction kaise hoga?',
        "answer": 'Students who believe assignment marks contain an error should submit a request for verification through the prescribed process.'
    },
    {
        "keywords": ['assignment rejected', 'resubmit assignment', 'invalid assignment'],
        "question": 'Mera assignment reject ho gaya hai. Kya karu?',
        "answer": 'Assignments may be rejected due to incorrect format, wrong session, incomplete submission or other academic reasons. Students should check the reason provided.'
    },
    {
        "keywords": ['assignment resubmission', 'repeat assignment', 'correction'],
        "question": 'Kya assignment dobara submit kar sakte hain?',
        "answer": 'Resubmission is allowed only according to IGNOU rules and specific circumstances. Students should follow instructions from the concerned authority.'
    },
    {
        "keywords": ['assignment missing', 'submission record not found'],
        "question": 'Maine assignment submit kiya tha lekin Study Centre me record nahi hai.',
        "answer": 'Students should provide submission proof so that the concerned centre can verify and trace the submission record.'
    },
    {
        "keywords": ['study centre not accepting assignment', 'submission issue'],
        "question": 'Study Centre mera assignment accept nahi kar raha hai.',
        "answer": 'Study Centres should follow IGNOU assignment submission guidelines. Students should contact the Regional Centre if they face difficulty in submission.'
    },
    {
        "keywords": ['track assignment', 'assignment status check'],
        "question": 'Assignment submission ka status kaise track karu?',
        "answer": 'Students can track assignment-related updates through available IGNOU systems or by contacting their Study Centre/Regional Centre.'
    },
    {
        "keywords": ['wrong study centre', 'assignment transfer', 'submission mistake'],
        "question": 'Maine assignment galat Study Centre me submit kar diya. Kya hoga?',
        "answer": 'Students should immediately inform the concerned centres. Transfer or acceptance depends on verification and applicable procedures.'
    },
    {
        "keywords": ['online assignment', 'lms submission', 'digital assignment'],
        "question": 'Online programme ke students assignment kaise submit karein?',
        "answer": 'Online programme assignment submission procedure depends on the instructions issued for the specific programme. Students should follow the designated online learning platform or submission process.'
    },
    {
        "keywords": ['project vs assignment', 'dissertation', 'academic submission'],
        "question": 'Project report aur assignment me kya difference hai?',
        "answer": 'Assignments are regular course-based academic tasks, while projects/dissertations are separate academic requirements applicable to specific programmes. Students should follow their programme guidelines.'
    },
    {
        "keywords": ['practical assignment', 'practical course', 'submission'],
        "question": 'Practical assignment kaise submit karna hai?',
        "answer": 'Practical assignments must be submitted according to programme-specific instructions through the designated Study Centre or online system wherever applicable.'
    },
    {
        "keywords": ['field work report', 'internship report', 'practical work'],
        "question": 'Field work report kahan submit karna hai?',
        "answer": 'Field work reports are submitted according to the requirements of the concerned programme and instructions issued by the School/Study Centre.'
    },
    {
        "keywords": ['foreign student assignment', 'overseas submission'],
        "question": 'International students assignment kaise submit karein?',
        "answer": 'International learners should follow the assignment submission procedure applicable to their region and programme. They should contact the concerned support authority for specific instructions.'
    },
    {
        "keywords": ['defence assignment', 'army student submission'],
        "question": 'Defence personnel assignment submit kaise karenge?',
        "answer": 'Defence personnel can submit assignments according to the normal IGNOU procedure through their allotted Study Centre or applicable support mechanism.'
    },
    {
        "keywords": ['prison assignment', 'jail learner', 'special centre'],
        "question": 'Jail inmates assignment kaise submit karte hain?',
        "answer": 'Jail inmate learners submit assignments through approved channels coordinated with authorized centres and concerned institutions.'
    },
    {
        "keywords": ['divyang assignment', 'accessibility support', 'special assistance'],
        "question": 'Divyang students ke liye assignment submission me kya facility hai?',
        "answer": 'IGNOU supports inclusive learning. Divyang learners may request appropriate support facilities according to applicable guidelines.'
    },
    {
        "keywords": ['assignment language', 'hindi assignment', 'medium'],
        "question": 'Kya assignment kisi bhi language me likh sakte hain?',
        "answer": 'Assignment language should follow the medium and instructions applicable to the programme. Students should refer to programme guidelines before submission.'
    },
    {
        "keywords": ['plagiarism', 'original assignment', 'academic integrity'],
        "question": 'Assignment me plagiarism karne se kya problem hogi?',
        "answer": 'Students should prepare original assignments. Copying content without proper understanding or acknowledgement may affect evaluation according to academic standards.'
    },
    {
        "keywords": ['assignment eligibility', 'exam eligibility', 'assignment pending'],
        "question": 'Assignment submit kar diya hai lekin exam me eligible nahi dikha raha hai. Kya karu?',
        "answer": 'Assignment submission status is one of the requirements considered for academic processing. Students should verify that the assignment has been received and updated in records.'
    },
    {
        "keywords": ['assignment marks missing', 'result incomplete', 'grade card issue'],
        "question": 'Assignment marks result me include nahi hue hain.',
        "answer": 'Assignment marks are included after evaluation and data processing. Delay may occur due to pending evaluation or record updating.'
    },
    {
        "keywords": ['re-registration assignment', 'old assignment', 'new assignment'],
        "question": 'Re-registration ke baad purana assignment submit karna hai ya naya?',
        "answer": 'Assignment validity depends on programme session and applicable assignment guidelines. Students should always refer to the latest assignment booklet.'
    },
    {
        "keywords": ['old assignment', 'assignment validity', 'previous session'],
        "question": 'Kya purane assignment dobara use kar sakte hain?',
        "answer": 'Students should submit assignments that are valid for their current academic session as per IGNOU instructions. Old assignments may not be accepted if they are no longer valid.'
    },
    {
        "keywords": ['assignment improvement', 'increase marks', 'assignment recheck'],
        "question": 'Kya assignment marks improve kar sakte hain?',
        "answer": 'Assignment improvement or re-submission depends on IGNOU rules applicable to the programme and academic situation.'
    },
    {
        "keywords": ['lost receipt', 'assignment proof', 'submission confirmation'],
        "question": 'Assignment submission receipt kho gayi hai. Kya karu?',
        "answer": 'Students should maintain assignment submission proof. If the receipt is lost, they should contact the submission centre for verification.'
    },
    {
        "keywords": ['assignment grievance', 'complaint registration', 'igram'],
        "question": 'Assignment ke liye iGRAM par complaint kaise karein?',
        "answer": 'Students can register assignment-related grievances through the official grievance mechanism when normal support channels do not resolve the issue.'
    },
    {
        "keywords": ['rc no response', 'pending complaint', 'escalation'],
        "question": 'Regional Centre reply nahi de raha hai. Kya karu?',
        "answer": 'Students should allow reasonable response time and follow the official escalation process if their issue remains unresolved.'
    },
    {
        "keywords": ['assignment complaint', 'final resolution', 'grievance closure'],
        "question": 'Assignment complaint ka final solution kaise milega?',
        "answer": 'Students should first approach the concerned Study Centre/Regional Centre. If unresolved, the matter may be escalated through the official grievance system.'
    },
    {
        "keywords": ['assignment information', 'assignment guide', 'student support'],
        "question": 'Assignment se related sabhi information ek jagah kahan milegi?',
        "answer": 'Students should refer to official IGNOU assignment guidelines, programme information and notifications for updated instructions.'
    },
    {
        "keywords": ['tee form', 'exam registration', 'term end examination'],
        "question": 'IGNOU Term End Examination (TEE) ke liye form kaise bharna hai?',
        "answer": 'Students must submit the Term End Examination form through the official IGNOU examination portal during the notified examination schedule. Students should ensure that they fulfil eligibility requirements before applying.'
    },
    {
        "keywords": ['exam form last date', 'tee schedule', 'submission deadline'],
        "question": 'IGNOU exam form ki last date kya hai?',
        "answer": 'Examination form submission dates are announced through official IGNOU notifications. Students should check the latest schedule before submitting the form.'
    },
    {
        "keywords": ['exam form error', 'unable to submit exam form'],
        "question": 'Main exam form submit nahi kar pa raha hu. Kya karu?',
        "answer": 'Exam form submission problems may occur due to technical issues, incomplete details or payment-related problems. Students should verify all information before final submission.'
    },
    {
        "keywords": ['exam fee payment', 'failed transaction', 'payment issue'],
        "question": 'Exam fee payment fail ho gaya hai. Kya karu?',
        "answer": 'Payment failure cases should be checked through transaction status. Students should avoid repeated payments until the previous transaction status is confirmed.'
    },
    {
        "keywords": ['money deducted exam fee', 'payment pending', 'exam registration'],
        "question": 'Paisa kat gaya lekin exam form submit nahi hua.',
        "answer": 'If payment is deducted but examination form is not confirmed, students should wait for transaction verification and provide payment proof if required.'
    },
    {
        "keywords": ['exam form confirmation', 'acknowledgement', 'exam receipt'],
        "question": 'Kaise pata chalega mera exam form submit ho gaya hai?',
        "answer": 'Successful examination form submission is confirmed through acknowledgement/receipt generated after submission. Students should save this record.'
    },
    {
        "keywords": ['exam course correction', 'change subject', 'exam form edit'],
        "question": 'Kya main exam form submit karne ke baad course change kar sakta hu?',
        "answer": 'Changes in examination form depend on IGNOU examination rules and the correction facility available during the examination cycle.'
    },
    {
        "keywords": ['wrong course selection', 'exam correction', 'subject change'],
        "question": 'Exam form me galat subject/course select ho gaya hai.',
        "answer": 'Students should report incorrect course selection immediately. Correction depends on the applicable correction window and IGNOU rules.'
    },
    {
        "keywords": ['assignment pending', 'exam eligibility', 'tee requirement'],
        "question": 'Kya assignment submit kiye bina exam de sakte hain?',
        "answer": 'Assignment submission is an important academic requirement for many programmes. Students should verify eligibility requirements before appearing in examinations.'
    },
    {
        "keywords": ['tee date', 'exam schedule', 'ignou examination'],
        "question": 'IGNOU TEE kab hoti hai?',
        "answer": 'IGNOU conducts Term End Examinations according to the notified examination schedule. Students should check official notifications for current examination dates.'
    },
    {
        "keywords": ['admit card', 'hall ticket', 'exam entry card'],
        "question": 'IGNOU admit card kaise download karu?',
        "answer": 'IGNOU releases admit cards/hall tickets through the official examination portal before the Term End Examination. Students should download and verify all details.'
    },
    {
        "keywords": ['admit card not available', 'hall ticket issue'],
        "question": 'Mera admit card download nahi ho raha hai. Kya karu?',
        "answer": 'Admit card availability depends on examination form submission, eligibility and processing status. Students should verify their details before raising a request.'
    },
    {
        "keywords": ['admit card correction', 'name correction', 'exam details'],
        "question": 'Admit card me mera naam ya details galat hai.',
        "answer": 'Students should report errors in admit card details to the concerned examination authority for verification and correction.'
    },
    {
        "keywords": ['exam centre', 'exam location', 'centre address'],
        "question": 'Exam centre ka address kaise pata chalega?',
        "answer": 'Examination centre details are mentioned in the admit card and examination-related notifications. Students should verify centre information before examination.'
    },
    {
        "keywords": ['change exam centre', 'centre transfer', 'exam location change'],
        "question": 'Kya exam centre change kar sakte hain?',
        "answer": 'Examination centre changes are allowed only according to IGNOU rules and availability. Students should submit requests within the permitted period, if applicable.'
    },
    {
        "keywords": ['date sheet', 'exam timetable', 'tee schedule'],
        "question": 'Date sheet kaise check kar sakta hu?',
        "answer": 'IGNOU publishes examination date sheets through official channels before the examination session. Students should verify their course-wise schedule.'
    },
    {
        "keywords": ['exam clash', 'same day exam', 'timetable issue'],
        "question": 'Mere do exams ek hi din aa gaye hain. Kya karu?',
        "answer": 'Examination clashes should be reported to the concerned examination authority with complete course details. Resolution depends on applicable examination rules.'
    },
    {
        "keywords": ['back paper', 'pending exam', 'reappear exam'],
        "question": 'Back paper exam ka form kaise bharen?',
        "answer": 'Students who have pending courses may apply for examinations according to IGNOU examination schedules and eligibility rules.'
    },
    {
        "keywords": ['practical exam date', 'practical schedule', 'lab exam'],
        "question": 'Practical examination ki date kaise milegi?',
        "answer": 'Practical examination schedules are communicated through the concerned Study Centre/Regional Centre or programme-specific channels.'
    },
    {
        "keywords": ['project exam', 'dissertation', 'viva', 'evaluation'],
        "question": 'Project/dissertation examination ka process kya hai?',
        "answer": 'Project/dissertation evaluation procedures depend on the programme requirements and instructions issued by the concerned School.'
    },
    {
        "keywords": ['exam centre missing', 'centre not allotted', 'tee centre'],
        "question": 'Mera exam centre allot nahi hua hai. Kya karu?',
        "answer": 'Examination centre allotment is processed after examination form submission and verification. Students should check their examination status and contact the concerned authority if the centre is not displayed.'
    },
    {
        "keywords": ['wrong exam centre', 'centre correction', 'hall ticket error'],
        "question": 'Admit card me galat exam centre show ho raha hai.',
        "answer": 'Students should immediately report incorrect examination centre details with supporting information for verification.'
    },
    {
        "keywords": ['overseas exam', 'foreign centre', 'international student exam'],
        "question": 'Foreign country se IGNOU exam kaise de sakte hain?',
        "answer": 'International students may appear through approved examination arrangements available for overseas learners. Students should follow instructions issued for international examination centres.'
    },
    {
        "keywords": ['defence exam', 'army student examination'],
        "question": 'Defence personnel ke liye examination facility kya hai?',
        "answer": 'Defence personnel enrolled with IGNOU follow the standard examination process. Special arrangements may be provided according to applicable guidelines.'
    },
    {
        "keywords": ['prison exam', 'jail learner exam', 'special centre'],
        "question": 'Jail inmates IGNOU exam kaise dete hain?',
        "answer": 'Examination arrangements for jail inmate learners are coordinated through approved special centres and concerned authorities.'
    },
    {
        "keywords": ['divyang exam', 'scribe facility', 'accessibility support'],
        "question": 'Divyang students ke liye exam me kya suvidha hai?',
        "answer": 'IGNOU provides support facilities for eligible Divyang learners according to applicable guidelines, including accessibility assistance wherever approved.'
    },
    {
        "keywords": ['exam fee refund', 'payment reversal', 'refund request'],
        "question": 'Exam fee refund kaise milega?',
        "answer": 'Examination fee refund is processed only in cases covered under applicable IGNOU rules. Students should submit requests with complete payment details.'
    },
    {
        "keywords": ['duplicate exam form', 'multiple payment', 'exam registration'],
        "question": 'Maine exam form do baar submit kar diya hai. Kya karu?',
        "answer": 'Duplicate examination form submissions should be reported for verification. Students should not submit unnecessary repeated requests.'
    },
    {
        "keywords": ['exam registration pending', 'payment verification', 'exam status'],
        "question": 'Mera exam registration pending dikha raha hai.',
        "answer": 'Pending examination registration may occur due to payment verification, processing delay or incomplete submission.'
    },
    {
        "keywords": ['exam portal error', 'website problem', 'technical issue'],
        "question": 'IGNOU exam portal open nahi ho raha hai.',
        "answer": 'Portal access problems may occur due to technical issues, maintenance or heavy traffic. Students should try basic troubleshooting before reporting.'
    },
    {
        "keywords": ['exam reporting time', 'exam instructions', 'centre entry'],
        "question": 'Exam centre par kitne time pehle pahunchna chahiye?',
        "answer": 'Students should reach the examination centre well before the scheduled examination time to complete verification procedures and avoid inconvenience.'
    },
    {
        "keywords": ['exam documents', 'admit card', 'id proof'],
        "question": 'Exam dene ke liye kaun-kaun se documents le jana zaroori hai?',
        "answer": 'Students should carry their admit card and valid identity proof as required for examination entry. Additional documents may be required for specific courses.'
    },
    {
        "keywords": ['admit card missing', 'exam entry problem'],
        "question": 'Agar exam ke din admit card nahi ho to kya karu?',
        "answer": 'Students should contact the examination centre authorities immediately. Entry decisions are taken according to examination rules and verification requirements.'
    },
    {
        "keywords": ['exam attendance', 'absent status', 'attendance correction'],
        "question": 'Main exam me present tha lekin attendance issue dikha raha hai.',
        "answer": 'Attendance records are maintained through examination processes. Students should report discrepancies with supporting details.'
    },
    {
        "keywords": ['missed exam', 'absent paper', 'next tee'],
        "question": 'Main exam nahi de paya. Ab kya karu?',
        "answer": 'Students who could not appear in an examination may appear in a future examination session subject to programme rules and eligibility.'
    },
    {
        "keywords": ['medical reason exam', 'special request', 'exam absence'],
        "question": 'Medical emergency ki wajah se exam miss ho gaya. Kya special chance milega?',
        "answer": 'Requests due to medical or emergency reasons are considered according to applicable IGNOU rules. Students should submit supporting documents if required.'
    },
    {
        "keywords": ['wrong question paper', 'missing paper', 'exam issue'],
        "question": 'Exam me question paper nahi mila ya galat paper mila. Kya karu?',
        "answer": 'Students should immediately inform the examination centre superintendent during the examination so that necessary action can be taken.'
    },
    {
        "keywords": ['answer sheet issue', 'exam complaint', 'evaluation query'],
        "question": 'Exam answer sheet se related complaint kaise karein?',
        "answer": 'Examination answer sheets are evaluated through established procedures. Any examination-related concern should be submitted through the prescribed process.'
    },
    {
        "keywords": ['re-exam', 'special exam', 'repeat examination'],
        "question": 'Kya re-examination ka option hota hai?',
        "answer": 'Re-examination opportunities depend on IGNOU rules and specific circumstances. Students should check official notifications for applicable provisions.'
    },
    {
        "keywords": ['exam guidelines', 'examination rules', 'tee instructions'],
        "question": 'IGNOU examination ke important instructions kahan milenge?',
        "answer": 'Examination instructions are issued through official IGNOU notifications, admit card instructions and examination-related communications.'
    },
    {
        "keywords": ['result pending after exam', 'result not generated', 'evaluation delay'],
        "question": 'Exam dene ke baad result generate nahi hua hai. Kya karu?',
        "answer": 'Examination results are published after completion of evaluation and data processing. Students should wait for the official result update schedule and verify their records.'
    },
    {
        "keywords": ['payment pending', 'exam fee status', 'transaction issue'],
        "question": 'Exam fee pay karne ke baad bhi payment pending dikha raha hai.',
        "answer": 'Payment status may take time to update due to transaction verification. Students should avoid making repeated payments until status is confirmed.'
    },
    {
        "keywords": ['backlog exam', 'pending paper', 'reappear'],
        "question": 'Backlog ya pending paper ke liye kya karna hota hai?',
        "answer": 'Students with pending courses can appear in subsequent Term End Examinations according to programme rules and eligibility.'
    },
    {
        "keywords": ['practical marks pending', 'lab marks', 'evaluation update'],
        "question": 'Practical exam ke marks update nahi hue hain.',
        "answer": 'Practical marks are updated after evaluation and submission by concerned authorities. Students should contact the Study Centre/Regional Centre for verification.'
    },
    {
        "keywords": ['project result', 'viva marks', 'dissertation update'],
        "question": 'Project viva ka result update nahi hua hai.',
        "answer": 'Project/dissertation evaluation requires submission, evaluation and processing by concerned authorities. Students should verify project status.'
    },
    {
        "keywords": ['exam centre complaint', 'centre issue', 'examination grievance'],
        "question": 'Exam centre par problem hui thi. Complaint kaise karein?',
        "answer": 'Students can report examination centre-related issues through the appropriate official channel with complete examination details.'
    },
    {
        "keywords": ['overseas exam problem', 'foreign student support'],
        "question": 'Overseas students ko exam me problem aa rahi hai. Kya karein?',
        "answer": 'International learners should contact the designated support authority for examination-related assistance according to overseas examination arrangements.'
    },
    {
        "keywords": ['defence exam support', 'military student issue'],
        "question": 'Defence personnel ke examination issue ka solution kaise milega?',
        "answer": 'Defence personnel should approach their concerned Regional Centre or designated support channel for examination-related assistance.'
    },
    {
        "keywords": ['jail exam complaint', 'prison learner support'],
        "question": 'Jail inmate student examination complaint kaise karein?',
        "answer": 'Examination issues of jail inmate learners are handled through approved special centres and concerned authorities.'
    },
    {
        "keywords": ['exam grievance', 'final resolution', 'examination complaint'],
        "question": 'Examination se related complaint ka final solution kaise milega?',
        "answer": 'Students should first contact the concerned examination support channel. If unresolved, they may escalate through Regional Centre and official grievance mechanisms.'
    },
    {
        "keywords": ['ignou result', 'result date', 'tee result'],
        "question": 'IGNOU result kab declare hoga?',
        "answer": 'IGNOU publishes Term End Examination results after completion of evaluation and data processing. Students should regularly check the official result portal and notifications.'
    },
    {
        "keywords": ['result not showing', 'result missing', 'tee result pending'],
        "question": 'Mera result show nahi ho raha hai. Kya karu?',
        "answer": 'Result availability depends on completion of evaluation and processing. Students should verify their examination details and wait for pending updates.'
    },
    {
        "keywords": ['missing marks', 'incomplete result', 'course marks pending'],
        "question": 'Result me kuch subjects ke marks nahi aaye hain.',
        "answer": 'Missing marks may occur due to pending evaluation, data entry or submission of assessment components. Students should verify the pending component.'
    },
    {
        "keywords": ['incomplete result', 'pending marks', 'grade card'],
        "question": 'Mera result incomplete dikha raha hai.',
        "answer": 'An incomplete result indicates that one or more academic components may be pending for processing. Students should check assignment, practical and examination status.'
    },
    {
        "keywords": ['grade card', 'marksheet', 'academic record'],
        "question": 'Grade card kaise check karein?',
        "answer": 'Students can view their grade card through the official IGNOU grade card facility using enrollment details.'
    },
    {
        "keywords": ['assignment marks missing', 'grade card update'],
        "question": 'Grade card me assignment marks nahi dikh rahe hain.',
        "answer": 'Assignment marks are updated after evaluation and processing by concerned authorities. Students should verify submission status before reporting.'
    },
    {
        "keywords": ['practical marks', 'lab marks', 'grade card issue'],
        "question": 'Grade card me practical marks nahi aaye hain.',
        "answer": 'Practical marks are updated after evaluation and submission by the concerned Study Centre or authority.'
    },
    {
        "keywords": ['result correction', 'marks error', 'evaluation mistake'],
        "question": 'Mera result galat show ho raha hai. Correction kaise hogi?',
        "answer": 'Students who find errors in their result record should submit a correction request with supporting details for verification.'
    },
    {
        "keywords": ['result delay', 'pending result', 'evaluation time'],
        "question": 'Result update hone me kitna time lagta hai?',
        "answer": 'Result updates depend on evaluation completion, verification and data processing. Students should follow official notifications for updates.'
    },
    {
        "keywords": ['result copy', 'marksheet', 'official record'],
        "question": 'Result ka printout ya official marksheet kaise milegi?',
        "answer": 'Students can access online result/grade card information through official systems. Official documents are issued according to IGNOU procedures.'
    },
    {
        "keywords": ['missing marks', 'result incomplete', 'marks pending'],
        "question": 'Result declare ho gaya hai lekin kuch marks missing hain. Kya karu?',
        "answer": 'Missing marks may occur due to pending evaluation, assessment submission or data processing. Students should verify the affected course details.'
    },
    {
        "keywords": ['result withheld', 'result blocked', 'verification pending'],
        "question": 'Mera result withheld dikha raha hai. Kya karu?',
        "answer": 'A withheld result may require verification of academic records, examination details or other pending requirements. Students should contact the concerned authority for clarification.'
    },
    {
        "keywords": ['wrong absent', 'attendance issue', 'result correction'],
        "question": 'Result me absent show ho raha hai jabki maine exam diya tha.',
        "answer": 'Students who find incorrect attendance/result status should report the matter with examination proof for verification.'
    },
    {
        "keywords": ['re-evaluation', 'answer copy review', 'marks review'],
        "question": 'IGNOU me re-evaluation kaise karte hain?',
        "answer": 'Students may apply for re-evaluation according to IGNOU rules and the notified procedure applicable to eligible courses.'
    },
    {
        "keywords": ['rechecking', 'revaluation difference', 'result review'],
        "question": 'Kya rechecking aur re-evaluation same hota hai?',
        "answer": 'Rechecking and re-evaluation are different processes. Students should refer to official IGNOU guidelines to understand the applicable procedure.'
    },
    {
        "keywords": ['improvement exam', 'improve marks', 'better grade'],
        "question": 'Improvement exam kya hota hai?',
        "answer": 'Improvement examination allows eligible students to improve performance according to applicable IGNOU regulations.'
    },
    {
        "keywords": ['failed subject', 'back paper', 'repeat exam'],
        "question": 'Ek subject me fail ho gaya hu. Ab kya karu?',
        "answer": 'Students with unsuccessful courses can appear in subsequent Term End Examinations subject to programme rules and validity period.'
    },
    {
        "keywords": ['final result pending', 'incomplete grade card'],
        "question": 'Pass hone ke baad bhi result me incomplete dikha raha hai.',
        "answer": 'Incomplete status may continue until all academic components are processed and updated in records.'
    },
    {
        "keywords": ['grade calculation', 'marks formula', 'evaluation system'],
        "question": 'IGNOU grade kaise calculate hota hai?',
        "answer": 'Grades are calculated according to IGNOU evaluation rules, considering applicable assessment components such as assignments and term-end examinations.'
    },
    {
        "keywords": ['division', 'class', 'final result calculation'],
        "question": 'IGNOU me division/class kaise decide hoti hai?',
        "answer": 'Final division/class is awarded according to the applicable academic regulations of the programme. Students should refer to programme guidelines.'
    },
    {
        "keywords": ['credit transfer', 'transferred credits', 'grade card update'],
        "question": 'Credit transfer ke baad result kaise update hota hai?',
        "answer": 'Credit transfer cases are processed according to IGNOU rules. After approval and processing, eligible credits are reflected in academic records.'
    },
    {
        "keywords": ['result correction after certificate', 'academic record correction'],
        "question": 'Certificate milne ke baad result me correction ho sakta hai kya?',
        "answer": 'Corrections in academic records after issuance of official documents are processed only through prescribed procedures and verification.'
    },
    {
        "keywords": ['name correction', 'result name error', 'student record'],
        "question": 'Result me mera naam galat show ho raha hai. Kya karu?',
        "answer": 'Name-related corrections require verification with official records and supporting documents.'
    },
    {
        "keywords": ['enrollment mismatch', 'grade card error'],
        "question": 'Grade card me enrollment number galat aa raha hai.',
        "answer": 'Any mismatch in enrollment details should be reported for verification and correction by the concerned authority.'
    },
    {
        "keywords": ['final semester result', 'completion result', 'pending evaluation'],
        "question": 'Final semester ka result delay ho raha hai. Kya karu?',
        "answer": 'Final semester results may require completion of all evaluation components, including assignments, practicals and projects where applicable.'
    },
    {
        "keywords": ['foreign student result', 'overseas result'],
        "question": 'International students ka result kaise check hota hai?',
        "answer": 'International students can access results through the official IGNOU result system using their enrollment details.'
    },
    {
        "keywords": ['online programme result', 'lms result'],
        "question": 'Online programme ka result kab aur kaise milega?',
        "answer": 'Online programme results are processed according to IGNOU evaluation procedures. Students can check updates through official result facilities.'
    },
    {
        "keywords": ['defence student result', 'military learner result'],
        "question": 'Defence personnel ka result pending hai. Kya karein?',
        "answer": 'Defence learners follow the standard result processing system. Pending cases should be reported through the concerned Regional Centre.'
    },
    {
        "keywords": ['jail student result', 'prison learner result'],
        "question": 'Jail inmate student ka result update nahi hua hai.',
        "answer": 'Result issues of jail inmate learners are handled through approved centres and concerned authorities.'
    },
    {
        "keywords": ['result grievance', 'complaint', 'pending result'],
        "question": 'Result ki complaint kaise register karein?',
        "answer": 'Students should first contact the concerned division or Regional Centre. If unresolved, they may register a grievance through the official grievance mechanism.'
    },
    {
        "keywords": ['completion status', 'programme completed', 'final update'],
        "question": 'Mere sabhi papers clear ho gaye hain lekin completion status update nahi hua hai. Kya karu?',
        "answer": 'Programme completion status is updated after verification of all academic requirements, including required credits, assignments, examinations and other components wherever applicable.'
    },
    {
        "keywords": ['final grade card', 'grade verification', 'marks record'],
        "question": 'Final grade card verify kaise kar sakta hu?',
        "answer": 'Students can verify their academic performance through the official grade card facility. Final verification should be done after completion of all required updates.'
    },
    {
        "keywords": ['evaluation appeal', 'marks appeal', 'academic grievance'],
        "question": 'Evaluation se related appeal kaise karein?',
        "answer": 'Students may submit evaluation-related requests according to IGNOU rules and available grievance mechanisms.'
    },
    {
        "keywords": ['result unresolved', 'pending complaint', 'escalation'],
        "question": 'Mera result update hone ke baad bhi problem solve nahi hui hai. Kya karu?',
        "answer": 'If the issue continues after result update, students should submit a detailed grievance with previous communication records for further review.'
    },
    {
        "keywords": ['result help', 'evaluation support', 'final solution'],
        "question": 'Result aur evaluation se related final help kahan milegi?',
        "answer": 'Students should approach the concerned academic/evaluation section first. For unresolved issues, the official grievance mechanism may be used.'
    },
    {
        "keywords": ['degree certificate', 'final certificate', 'certificate issue'],
        "question": 'IGNOU degree certificate kab milegi?',
        "answer": 'Degree certificates are issued after successful completion of the programme and after completion of required academic verification processes. Students should check official notifications regarding certificate distribution/dispatch.'
    },
    {
        "keywords": ['provisional certificate', 'temporary certificate'],
        "question": 'Provisional certificate kaise milega?',
        "answer": 'Eligible students may obtain provisional certification according to IGNOU procedures after completion of programme requirements.'
    },
    {
        "keywords": ['degree not received', 'certificate pending'],
        "question": 'Degree complete ho gayi hai lekin certificate nahi mila. Kya karu?',
        "answer": 'Students should first verify dispatch/distribution status and raise a request if the certificate has not been received after the prescribed period.'
    },
    {
        "keywords": ['convocation registration', 'degree ceremony'],
        "question": 'Convocation ke liye registration kaise karein?',
        "answer": 'Convocation registration is conducted according to official IGNOU notifications. Eligible students should register through the notified process.'
    },
    {
        "keywords": ['unable to attend convocation', 'degree dispatch'],
        "question": 'Convocation attend nahi kar paunga to degree kaise milegi?',
        "answer": 'Students unable to attend convocation may receive their certificates according to IGNOU’s prescribed dispatch procedure.'
    },
    {
        "keywords": ['diploma certificate', 'course completion'],
        "question": 'IGNOU diploma certificate kab milega?',
        "answer": 'Diploma certificates are issued after successful completion and verification of programme requirements.'
    },
    {
        "keywords": ['certificate name correction', 'document correction'],
        "question": 'Certificate me naam galat hai. Correction kaise hogi?',
        "answer": 'Name correction in certificates requires verification and submission of supporting documents according to IGNOU procedures.'
    },
    {
        "keywords": ['certificate delivery', 'address update', 'dispatch issue'],
        "question": 'Address change ke karan certificate nahi mila. Kya karu?',
        "answer": 'Students should ensure that their address details are updated before certificate dispatch. Any delivery issue should be reported with correct details.'
    },
    {
        "keywords": ['migration certificate', 'university transfer'],
        "question": 'Migration certificate kaise milega?',
        "answer": 'Migration certificate is issued according to IGNOU procedures for eligible students who require it for further academic purposes.'
    },
    {
        "keywords": ['transcript', 'academic record', 'marksheet'],
        "question": 'Transcript kaise apply karein?',
        "answer": 'Students requiring official academic transcripts should apply through the prescribed IGNOU transcript service procedure.'
    },
    {
        "keywords": ['duplicate degree', 'lost certificate', 'replacement certificate'],
        "question": 'Degree certificate kho gaya hai. Duplicate kaise milega?',
        "answer": 'Students who have lost their original certificate may apply for a duplicate certificate according to IGNOU procedures.'
    },
    {
        "keywords": ['duplicate marksheet', 'lost grade card'],
        "question": 'Marksheet kho gayi hai. Duplicate marksheet kaise milegi?',
        "answer": 'Students can request duplicate academic documents through the prescribed IGNOU process after verification.'
    },
    {
        "keywords": ['degree dispatch', 'certificate tracking'],
        "question": 'Degree certificate dispatch status kaise check karein?',
        "answer": 'Certificate dispatch information depends on the available tracking mechanism and official communication issued by IGNOU.'
    },
    {
        "keywords": ['certificate not delivered', 'dispatch problem'],
        "question": 'Mera certificate address par deliver nahi hua hai. Kya karu?',
        "answer": 'Delivery issues should be reported after verifying registered address and dispatch details.'
    },
    {
        "keywords": ['foreign student certificate', 'overseas delivery'],
        "question": 'International student ko certificate kaise milega?',
        "answer": 'International students receive certificates according to IGNOU’s prescribed certificate delivery process applicable to overseas learners.'
    },
    {
        "keywords": ['online course certificate', 'digital programme certificate'],
        "question": 'Online programme complete karne ke baad certificate milega?',
        "answer": 'Students completing eligible online programmes receive certificates according to IGNOU academic and certification procedures.'
    },
    {
        "keywords": ['certificate verification', 'employer verification'],
        "question": 'Employer verification ke liye IGNOU certificate kaise verify hoga?',
        "answer": 'Certificate verification requests are processed through appropriate official channels. Employers or institutions should follow the prescribed verification procedure.'
    },
    {
        "keywords": ['foreign verification', 'embassy', 'overseas admission'],
        "question": 'Foreign university ke liye certificate verification kaise karayein?',
        "answer": 'Students requiring verification for foreign institutions should follow the official document verification process and provide required details.'
    },
    {
        "keywords": ['certificate attestation', 'document authentication'],
        "question": 'Certificate attestation ka process kya hai?',
        "answer": 'Attestation requirements depend on the purpose and authority requesting the document. Students should follow applicable official procedures.'
    },
    {
        "keywords": ['name change', 'legal correction', 'certificate update'],
        "question": 'Certificate me legal name change kaise karwayein?',
        "answer": 'Legal name changes require submission of valid legal documents and verification according to IGNOU rules.'
    },
    {
        "keywords": ['certificate correction', 'updated result', 'document revision'],
        "question": 'Result update hone ke baad certificate me correction kaise hoga?',
        "answer": 'If academic records are updated after certificate processing, any required correction will be handled according to IGNOU verification procedures.'
    },
    {
        "keywords": ['provisional certificate pending', 'certificate delay'],
        "question": 'Provisional certificate abhi tak nahi mila hai. Kya karu?',
        "answer": 'Students should verify completion status and follow the prescribed provisional certificate request process if applicable.'
    },
    {
        "keywords": ['convocation degree pending', 'ceremony certificate'],
        "question": 'Convocation attend kiya tha lekin degree nahi mili. Kya karu?',
        "answer": 'Students should report non-receipt of degree after convocation with complete details for verification.'
    },
    {
        "keywords": ['multiple certificates', 'multiple programmes'],
        "question": 'Ek se zyada IGNOU programme complete kiye hain. Certificate kaise milega?',
        "answer": 'Certificates are issued according to completion of each eligible programme and applicable IGNOU procedures.'
    },
    {
        "keywords": ['incomplete programme', 'certificate eligibility'],
        "question": 'Programme complete nahi hua hai to certificate milega kya?',
        "answer": 'Official certificates are issued after successful completion of prescribed programme requirements.'
    },
    {
        "keywords": ['defence certificate', 'military student degree'],
        "question": 'Defence personnel ko degree certificate kaise milega?',
        "answer": 'Defence learners receive certificates through the same academic process with support from concerned Regional Centres where required.'
    },
    {
        "keywords": ['prison learner certificate', 'jail student degree'],
        "question": 'Jail inmate student ka certificate kaise milega?',
        "answer": 'Certificates for jail inmate learners are processed through approved channels and concerned authorities.'
    },
    {
        "keywords": ['digital certificate', 'e-certificate', 'online document'],
        "question": 'Digital certificate ya online certificate mil sakta hai kya?',
        "answer": 'Availability of digital certificates depends on IGNOU’s approved digital document services and applicable programmes.'
    },
    {
        "keywords": ['certificate complaint', 'degree issue', 'grievance'],
        "question": 'Certificate ke liye complaint kahan karein?',
        "answer": 'Students should contact the Certificate Division first. If the issue remains unresolved, they may use the official grievance mechanism.'
    },
    {
        "keywords": ['certificate resolution', 'final complaint', 'escalation'],
        "question": 'Certificate related issue ka final solution kaise milega?',
        "answer": 'Complete details and supporting documents help faster resolution of certificate-related issues. Students should follow the official escalation process.'
    },
    {
        "keywords": ['duplicate degree', 'duplicate certificate', 'replacement document'],
        "question": 'Duplicate certificate ke liye complete process kya hai?',
        "answer": 'Students requiring duplicate certificates must follow the prescribed IGNOU procedure after verification of student records.'
    },
    {
        "keywords": ['certificate pending', 'completed course certificate'],
        "question": 'Programme complete hone ke baad bhi certificate nahi mila hai.',
        "answer": 'Certificate issuance depends on completion verification and official processing schedules. Students should verify completion status and certificate records.'
    },
    {
        "keywords": ['convocation complaint', 'degree ceremony issue'],
        "question": 'Convocation se related complaint kaise solve hogi?',
        "answer": 'Convocation-related issues should be reported through the Convocation Cell or Certificate Division with complete details.'
    },
    {
        "keywords": ['certificate delivery', 'dispatch problem', 'missing document'],
        "question": 'Certificate delivery problem kaise solve hoga?',
        "answer": 'Delivery issues are resolved after verification of dispatch details, address records and student information.'
    },
    {
        "keywords": ['certificate help', 'degree support', 'final resolution'],
        "question": 'Certificate aur convocation se related final help kahan milegi?',
        "answer": 'Students should contact the concerned Certificate/Convocation section first. Unresolved issues may be escalated through IGNOU grievance channels.'
    },
    {
        "keywords": ['ignou complaint', 'grievance registration', 'student problem'],
        "question": 'IGNOU me complaint kaise register karein?',
        "answer": 'Students can register their complaints through the official IGNOU grievance redressal mechanism. Students should provide complete details so that the issue can be forwarded to the concerned section.'
    },
    {
        "keywords": ['igram', 'online complaint', 'grievance portal'],
        "question": 'iGRAM portal kya hai aur iska use kaise karein?',
        "answer": 'iGRAM is an online grievance management system designed to help students submit and track their complaints related to IGNOU services.'
    },
    {
        "keywords": ['complaint status', 'grievance tracking'],
        "question": 'Complaint submit karne ke baad status kaise check karein?',
        "answer": 'Students can track grievance progress using the reference number generated after successful submission.'
    },
    {
        "keywords": ['no response', 'pending complaint', 'grievance delay'],
        "question": 'Meri complaint ka reply nahi aaya hai. Kya karu?',
        "answer": 'Response time depends on the nature of the issue and the concerned division. Students should wait for processing time and follow up through official channels.'
    },
    {
        "keywords": ['closed complaint', 'reopen grievance', 'unsatisfied response'],
        "question": 'Complaint close ho gayi hai lekin problem solve nahi hui. Kya karein?',
        "answer": 'If a student is not satisfied with grievance resolution, they may request review/reopening through the appropriate grievance channel.'
    },
    {
        "keywords": ['cpgrams', 'government complaint', 'escalation'],
        "question": 'CPGRAMS par IGNOU ki complaint kaise karein?',
        "answer": 'Students may use the government grievance mechanism for matters requiring escalation after using available institutional grievance channels.'
    },
    {
        "keywords": ['complaint documents', 'proof upload', 'grievance support'],
        "question": 'Complaint ke liye kaun se documents upload karne chahiye?',
        "answer": 'Students should upload documents relevant to their issue to help faster verification and resolution.'
    },
    {
        "keywords": ['duplicate complaint', 'follow-up grievance'],
        "question": 'Ek hi problem ke liye baar-baar complaint kar sakte hain kya?',
        "answer": 'Students should avoid duplicate complaints for the same issue. They should use the existing grievance reference number for follow-up.'
    },
    {
        "keywords": ['complaint routing', 'department', 'grievance forwarding'],
        "question": 'Complaint kis department ko bheji jati hai?',
        "answer": 'Grievances are forwarded to the concerned IGNOU division based on the nature of the issue.'
    },
    {
        "keywords": ['ssc help', 'student support', 'ignou assistance'],
        "question": 'Student Service Centre (SSC) se help kaise milegi?',
        "answer": 'SSC provides support guidance for student service-related issues and helps route unresolved matters to appropriate divisions.'
    },
    {
        "keywords": ['pending grievance', 'delayed complaint', 'unresolved issue'],
        "question": 'Meri grievance bahut din se pending hai. Kya karu?',
        "answer": 'Some grievances require verification from multiple sections and may take additional processing time. Students should track status and follow the official escalation process if delayed.'
    },
    {
        "keywords": ['wrong department complaint', 'grievance transfer'],
        "question": 'Meri complaint galat department ko chali gayi hai. Kya karu?',
        "answer": 'Grievances are reviewed and forwarded to the appropriate section based on the issue category. Students should provide correct details for proper routing.'
    },
    {
        "keywords": ['grievance appeal', 'unsatisfied complaint', 'review request'],
        "question": 'Complaint ke decision se santusht nahi hu. Appeal kaise karein?',
        "answer": 'Students who are not satisfied with the response may submit a review request through the appropriate grievance mechanism.'
    },
    {
        "keywords": ['student feedback', 'service review', 'grievance feedback'],
        "question": 'Complaint solve hone ke baad feedback kaise dein?',
        "answer": 'Student feedback helps improve service delivery. Students may provide feedback through available official feedback mechanisms.'
    },
    {
        "keywords": ['academic grievance', 'course issue', 'student complaint'],
        "question": 'Academic problem ke liye grievance kaise karein?',
        "answer": 'Academic issues should be submitted with complete programme and course details so that they can be examined by the concerned academic authority.'
    },
    {
        "keywords": ['portal error', 'website problem', 'technical complaint'],
        "question": 'Portal par technical problem ki complaint kaise karein?',
        "answer": 'Technical issues related to IGNOU portals should be reported with screenshots and error details for faster resolution.'
    },
    {
        "keywords": ['admission complaint', 'registration issue'],
        "question": 'Admission related complaint kahan karein?',
        "answer": 'Admission-related grievances should be submitted through the appropriate admission support channels with registration details.'
    },
    {
        "keywords": ['assignment complaint', 'marks issue', 'submission grievance'],
        "question": 'Assignment related complaint kaise karein?',
        "answer": 'Assignment issues should first be reported to the Study Centre/Regional Centre and may be escalated through the grievance system if unresolved.'
    },
    {
        "keywords": ['exam complaint', 'tee grievance', 'hall ticket issue'],
        "question": 'Examination complaint kaise register karein?',
        "answer": 'Examination-related complaints should include complete examination details for verification by the Student Evaluation Division.'
    },
    {
        "keywords": ['result complaint', 'marks grievance', 'grade card issue'],
        "question": 'Result related complaint kaise solve karayein?',
        "answer": 'Result-related complaints should be submitted with complete academic details and supporting proof for verification.'
    },
    {
        "keywords": ['certificate complaint', 'degree issue', 'document problem'],
        "question": 'Certificate related complaint kaise karein?',
        "answer": 'Certificate-related complaints should be submitted with complete academic and document details for verification by the concerned Certificate Division.'
    },
    {
        "keywords": ['scholarship complaint', 'financial support', 'payment issue'],
        "question": 'Scholarship related complaint kahan karein?',
        "answer": 'Scholarship-related issues should be reported with complete financial and eligibility details through the appropriate support channel.'
    },
    {
        "keywords": ['fee complaint', 'payment failed', 'transaction issue'],
        "question": 'Fee payment related complaint kaise solve hogi?',
        "answer": 'Payment issues require transaction verification. Students should provide payment details and avoid making repeated payments until status is confirmed.'
    },
    {
        "keywords": ['regional centre complaint', 'local support issue'],
        "question": 'Regional Centre ke against complaint kaise karein?',
        "answer": 'Students should first contact the concerned Regional Centre for local academic support. Unresolved issues may be escalated through official grievance channels.'
    },
    {
        "keywords": ['study centre complaint', 'counselling issue'],
        "question": 'Study Centre ke against complaint kaise karein?',
        "answer": 'Study Centre-related issues should be reported with complete details for review and appropriate action.'
    },
    {
        "keywords": ['foreign student complaint', 'overseas support'],
        "question": 'International student grievance kaise solve hogi?',
        "answer": 'International students may submit grievances through appropriate channels with country, programme and academic details.'
    },
    {
        "keywords": ['divyang support', 'accessibility grievance'],
        "question": 'Divyang student ke liye special complaint support hai kya?',
        "answer": 'Divyang learners can report accessibility, examination or academic support issues through official grievance channels.'
    },
    {
        "keywords": ['escalation process', 'complaint hierarchy'],
        "question": 'Grievance ko kis level par escalate kiya ja sakta hai?',
        "answer": 'Students should follow the defined escalation structure to ensure systematic resolution of complaints.'
    },
    {
        "keywords": ['ai chatbot', 'automated help', 'digital support'],
        "question": 'AI chatbot meri complaint kaise solve karega?',
        "answer": 'AI chatbot can provide instant guidance, identify issue category, provide procedures and direct students to the correct service channel.'
    },
    {
        "keywords": ['complaint closure', 'grievance resolution', 'final status'],
        "question": 'Grievance ka final closure kaise hota hai?',
        "answer": 'A grievance is considered resolved after review by the concerned authority and communication of appropriate action or guidance to the student.'
    },
    {
        "keywords": ['regional centre', 'rc details', 'student centre'],
        "question": 'Mera Regional Centre kaunsa hai kaise pata chalega?',
        "answer": 'Regional Centre allocation is based on the details provided during admission and the learner’s selected area/location. Students can verify their Regional Centre through official student services.'
    },
    {
        "keywords": ['study centre', 'centre allocation', 'learner support'],
        "question": 'Study Centre kaise select ya check karein?',
        "answer": 'Study Centre details are allotted according to programme availability and learner location. Students should verify their allotted Study Centre through official records.'
    },
    {
        "keywords": ['change study centre', 'centre transfer'],
        "question": 'Mera Study Centre change karna hai. Kya process hai?',
        "answer": 'Study Centre change requests are considered according to programme availability, administrative guidelines and applicable procedures.'
    },
    {
        "keywords": ['change regional centre', 'rc transfer'],
        "question": 'Regional Centre change kaise karein?',
        "answer": 'Regional Centre change may be permitted according to IGNOU rules and administrative requirements. Students should contact their Regional Centre for guidance.'
    },
    {
        "keywords": ['counselling schedule', 'classes', 'academic support'],
        "question": 'Counselling classes kab hoti hain?',
        "answer": 'Counselling schedules are prepared by Study Centres and communicated to learners through appropriate channels.'
    },
    {
        "keywords": ['study centre contact', 'local support'],
        "question": 'Study Centre se contact kaise karein?',
        "answer": 'Students can contact their allotted Study Centre through details provided by IGNOU Regional Centre.'
    },
    {
        "keywords": ['study centre not responding', 'local complaint'],
        "question": 'Mera Study Centre response nahi de raha hai. Kya karu?',
        "answer": 'Students should first attempt contact through available channels and may approach the Regional Centre if support is not received.'
    },
    {
        "keywords": ['practical classes', 'lab session', 'practical centre'],
        "question": 'Practical classes kahan hoti hain?',
        "answer": 'Practical classes are conducted at designated Study Centres or approved locations as per programme requirements.'
    },
    {
        "keywords": ['assignment submission centre', 'assignment deposit'],
        "question": 'Assignment kahan submit karna hai?',
        "answer": 'Assignment submission location depends on programme instructions and the designated Study Centre/Regional Centre guidelines.'
    },
    {
        "keywords": ['regional centre help', 'academic support'],
        "question": 'Regional Centre se academic help kaise milegi?',
        "answer": 'Regional Centres provide learner support services including guidance, coordination with Study Centres and resolution of student issues.'
    },
    {
        "keywords": ['study centre closed', 'inactive centre', 'alternative centre'],
        "question": 'Mera Study Centre band ho gaya hai ya active nahi hai. Kya karu?',
        "answer": 'If a Study Centre becomes unavailable or inactive, the Regional Centre provides guidance regarding alternative arrangements for learners.'
    },
    {
        "keywords": ['counselling not conducted', 'class issue'],
        "question": 'Study Centre par counselling nahi ho rahi hai. Kya karein?',
        "answer": 'Counselling schedules are managed by Study Centres. Students should report non-availability to the Regional Centre for necessary action.'
    },
    {
        "keywords": ['practical class complaint', 'lab issue'],
        "question": 'Practical class nahi ho rahi hai. Complaint kaise karein?',
        "answer": 'Practical sessions are arranged according to programme requirements. Students should contact the Study Centre and Regional Centre for support.'
    },
    {
        "keywords": ['assignment collection', 'submission problem'],
        "question": 'Assignment collect nahi ho raha hai Study Centre par. Kya karu?',
        "answer": 'Assignment collection is handled according to Study Centre guidelines. Students should confirm submission instructions and report issues if required.'
    },
    {
        "keywords": ['attendance requirement', 'counselling attendance'],
        "question": 'Kya IGNOU me attendance compulsory hai?',
        "answer": 'Attendance requirements depend on programme components such as counselling, practicals, workshops and specific academic requirements.'
    },
    {
        "keywords": ['job transfer', 'relocation', 'centre change'],
        "question": 'Naukri ya transfer ke karan Study Centre change karna hai.',
        "answer": 'Learners who relocate may request Study Centre change according to availability and applicable IGNOU rules.'
    },
    {
        "keywords": ['rural learner', 'village student support'],
        "question": 'Rural area ke students ko local support kaise milega?',
        "answer": 'IGNOU provides learner support through Regional Centres and Study Centres established at various locations to assist learners.'
    },
    {
        "keywords": ['senior citizen learner', 'special support'],
        "question": 'Senior citizen students ke liye Study Centre support available hai?',
        "answer": 'Senior citizen learners can access available learner support services through Regional Centres and Study Centres.'
    },
    {
        "keywords": ['defence learner', 'military support'],
        "question": 'Defence personnel ko Study Centre support kaise milega?',
        "answer": 'Defence personnel learners can coordinate with their Regional Centre and Study Centre for academic assistance.'
    },
    {
        "keywords": ['regional centre grievance', 'rc complaint'],
        "question": 'Regional Centre ke against complaint kaise karein?',
        "answer": 'Students should first communicate with the Regional Centre. Unresolved issues may be escalated through IGNOU grievance channels.'
    },
    {
        "keywords": ['study centre change pending', 'transfer request'],
        "question": 'Study Centre change approve nahi hua hai. Kya karu?',
        "answer": 'Study Centre change requests depend on programme availability, administrative approval and applicable guidelines. Students should check the status with the Regional Centre.'
    },
    {
        "keywords": ['wrong study centre', 'centre allocation error'],
        "question": 'Admission me galat Study Centre allot ho gaya hai. Correction kaise hogi?',
        "answer": 'Students should report incorrect Study Centre allocation to the concerned Regional Centre for verification and necessary action.'
    },
    {
        "keywords": ['counselling timetable', 'class schedule'],
        "question": 'Counselling schedule ki information kaise milegi?',
        "answer": 'Counselling schedules are communicated by Study Centres through available official channels. Students should remain connected with their allotted centre.'
    },
    {
        "keywords": ['local support', 'learner assistance'],
        "question": 'Local student support ke liye kisse contact karein?',
        "answer": 'Students should contact their allotted Study Centre for local academic assistance and Regional Centre for administrative support.'
    },
    {
        "keywords": ['rc support', 'study centre help', 'final solution'],
        "question": 'Regional Centre aur Study Centre se related final help kaise milegi?',
        "answer": 'Students should approach the appropriate centre with complete details. Unresolved matters can be escalated through official grievance channels.'
    },
    {
        "keywords": ['ignou scholarship', 'financial aid', 'student support'],
        "question": 'IGNOU me scholarship milti hai kya?',
        "answer": 'IGNOU students may avail scholarships and financial assistance schemes offered by Government agencies and other eligible authorities. Availability depends on eligibility criteria and applicable scheme guidelines.'
    },
    {
        "keywords": ['nsp scholarship', 'government scholarship', 'application'],
        "question": 'National Scholarship Portal (NSP) par IGNOU student apply kar sakta hai kya?',
        "answer": 'Eligible IGNOU learners may apply for scholarships available through the National Scholarship Portal as per scheme rules and eligibility conditions.'
    },
    {
        "keywords": ['scholarship eligibility', 'criteria', 'financial assistance'],
        "question": 'Scholarship ke liye eligibility kya hai?',
        "answer": 'Eligibility depends on the specific scholarship scheme, including criteria related to category, income, academic requirements and other conditions.'
    },
    {
        "keywords": ['scholarship form error', 'application problem'],
        "question": 'Scholarship form submit nahi ho raha hai. Kya karu?',
        "answer": 'Technical issues during scholarship application should be checked and reported through the concerned scholarship portal/support channel.'
    },
    {
        "keywords": ['scholarship status', 'application tracking'],
        "question": 'Scholarship status kaise check karein?',
        "answer": 'Students can check scholarship status through the concerned scholarship portal using their application details.'
    },
    {
        "keywords": ['scholarship payment pending', 'fund not received'],
        "question": 'Scholarship approve ho gayi hai lekin paisa nahi mila. Kya karu?',
        "answer": 'Payment delays may occur due to verification, banking or fund release processes. Students should check payment status and bank details.'
    },
    {
        "keywords": ['bank payment issue', 'scholarship transfer'],
        "question": 'Bank account me scholarship payment nahi aaya hai.',
        "answer": 'Students should verify that bank details provided in the scholarship application are correct and active.'
    },
    {
        "keywords": ['fee reimbursement', 'fee support'],
        "question": 'Fee reimbursement ke liye kya process hai?',
        "answer": 'Fee reimbursement depends on applicable government or institutional schemes and their eligibility conditions.'
    },
    {
        "keywords": ['sc scholarship', 'st scholarship', 'obc scholarship'],
        "question": 'SC/ST/OBC category students ke liye scholarship available hai kya?',
        "answer": 'Category-based scholarships may be available through government schemes subject to eligibility conditions and applicable rules.'
    },
    {
        "keywords": ['scholarship deadline', 'application date'],
        "question": 'Scholarship ki last date kaise pata chalegi?',
        "answer": 'Scholarship deadlines are announced by the concerned scholarship authority. Students should regularly check official notifications and portals.'
    },
    {
        "keywords": ['scholarship verification', 'document pending'],
        "question": 'Scholarship document verification nahi hua hai. Kya karu?',
        "answer": 'Scholarship applications require verification of submitted information and documents by the concerned authority. Students should check verification status and follow instructions.'
    },
    {
        "keywords": ['scholarship rejected', 'application failed'],
        "question": 'Scholarship application reject ho gayi hai. Kya karein?',
        "answer": 'Rejection reasons depend on scheme rules, eligibility criteria or document verification. Students should check the reason mentioned and take appropriate action if permitted.'
    },
    {
        "keywords": ['scholarship renewal', 'continue scholarship'],
        "question": 'Scholarship renewal kaise hoti hai?',
        "answer": 'Renewal depends on the rules of the concerned scholarship scheme and continued eligibility of the student.'
    },
    {
        "keywords": ['fee concession', 'fee waiver', 'financial support'],
        "question": 'IGNOU me fee concession milti hai kya?',
        "answer": 'Fee concession depends on applicable government policies, institutional provisions and eligibility conditions. Students should check current notifications.'
    },
    {
        "keywords": ['divyang scholarship', 'disability support'],
        "question": 'Divyang students ke liye financial assistance available hai kya?',
        "answer": 'Eligible Divyang learners may apply for available government financial assistance schemes according to applicable guidelines.'
    },
    {
        "keywords": ['defence scholarship', 'military student support'],
        "question": 'Defence personnel students ke liye financial support available hai kya?',
        "answer": 'Defence learners may explore financial assistance schemes available through government or service-related channels subject to eligibility.'
    },
    {
        "keywords": ['foreign student scholarship', 'overseas financial support'],
        "question": 'International students ke liye scholarship ya financial aid available hai kya?',
        "answer": 'Financial assistance for international students depends on applicable schemes, agreements and eligibility conditions.'
    },
    {
        "keywords": ['scholarship amount issue', 'payment discrepancy'],
        "question": 'Scholarship ka paisa kam mila hai ya galat amount aaya hai. Kya karein?',
        "answer": 'Scholarship amounts are determined by the concerned scheme authority. Students should verify payment details and contact the responsible authority for clarification.'
    },
    {
        "keywords": ['scholarship complaint', 'financial grievance'],
        "question": 'Scholarship se related complaint kaise karein?',
        "answer": 'Scholarship grievances should be submitted with complete application and payment details through the appropriate channel.'
    },
    {
        "keywords": ['scholarship help', 'financial assistance', 'final resolution'],
        "question": 'Scholarship aur financial support ke liye final help kahan milegi?',
        "answer": 'Students should first contact the concerned scholarship authority or IGNOU support section. Unresolved matters may be escalated through official grievance channels.'
    },
    {
        "keywords": ['lms login', 'online class login', 'learner portal'],
        "question": 'IGNOU online programme ka LMS login kaise karein?',
        "answer": 'Online programme learners can access their learning platform using the credentials provided after successful registration/enrolment.'
    },
    {
        "keywords": ['forgot password', 'lms password reset'],
        "question": 'LMS ka username ya password bhool gaya hu. Kya karu?',
        "answer": 'Students can reset their password using the available password recovery option on the learning platform.'
    },
    {
        "keywords": ['lms login error', 'portal not working'],
        "question": 'LMS me login nahi ho raha hai.',
        "answer": 'Login issues may occur due to incorrect credentials, browser issues or technical problems. Students should verify details and try again.'
    },
    {
        "keywords": ['online class schedule', 'webinar', 'virtual class'],
        "question": 'Online classes ka schedule kahan milega?',
        "answer": 'Online class schedules are communicated through the learning platform and official programme notifications.'
    },
    {
        "keywords": ['recorded lecture', 'video class', 'e-learning'],
        "question": 'Recorded lectures kaise dekhein?',
        "answer": 'Recorded lectures are made available through the designated online learning platform where applicable.'
    },
    {
        "keywords": ['digital material', 'e-content', 'online books'],
        "question": 'Digital study material kaha milega?',
        "answer": 'Online learners can access digital learning resources through approved IGNOU digital platforms.'
    },
    {
        "keywords": ['online assignment', 'upload assignment'],
        "question": 'Online assignment kaise submit karein?',
        "answer": 'Online assignment submission procedure depends on programme instructions. Students should submit through the prescribed platform within the notified deadline.'
    },
    {
        "keywords": ['assignment upload error', 'lms submission problem'],
        "question": 'Online assignment upload nahi ho raha hai. Kya karu?',
        "answer": 'Upload problems may occur due to file size, format or technical issues. Students should check requirements and retry.'
    },
    {
        "keywords": ['mobile learning', 'app access', 'online study'],
        "question": 'Mobile phone se online classes access kar sakte hain kya?',
        "answer": 'Students may access online learning resources through compatible mobile devices as per platform requirements.'
    },
    {
        "keywords": ['online certificate', 'programme completion'],
        "question": 'Online programme complete karne ke baad certificate kaise milega?',
        "answer": 'Certificates for completed online programmes are issued according to IGNOU academic and certification procedures.'
    },
    {
        "keywords": ['online exam', 'digital examination', 'test login'],
        "question": 'Online examination kaise hoti hai?',
        "answer": 'Online examination procedure depends on the programme guidelines and instructions issued by IGNOU. Students should follow official notifications carefully.'
    },
    {
        "keywords": ['online exam login', 'exam portal error'],
        "question": 'Online exam me login nahi ho raha hai. Kya karu?',
        "answer": 'Students should verify credentials and technical requirements before reporting login problems.'
    },
    {
        "keywords": ['course missing', 'lms course not visible'],
        "question": 'LMS me mera course show nahi ho raha hai.',
        "answer": 'Course visibility depends on programme activation and learner registration status. Students should verify enrolment and course mapping.'
    },
    {
        "keywords": ['digital content error', 'e-learning problem'],
        "question": 'Online study material open nahi ho raha hai.',
        "answer": 'Digital content access issues may occur due to technical reasons or platform problems.'
    },
    {
        "keywords": ['discussion forum', 'academic query'],
        "question": 'Discussion forum me question ka answer nahi mil raha hai.',
        "answer": 'Students should use available academic support channels and contact concerned faculty/support teams when required.'
    },
    {
        "keywords": ['video not playing', 'lecture problem'],
        "question": 'Video lecture chal nahi raha hai.',
        "answer": 'Video playback problems may occur due to internet speed, browser compatibility or device settings.'
    },
    {
        "keywords": ['audio problem', 'virtual class issue'],
        "question": 'Audio clear nahi aa raha hai online class me.',
        "answer": 'Students should check device and network settings before reporting audio-related issues.'
    },
    {
        "keywords": ['system requirement', 'online learning setup'],
        "question": 'Online programme ki technical requirements kya hain?',
        "answer": 'Students should use a compatible device, internet connection and supported software as specified for online learning platforms.'
    },
    {
        "keywords": ['online fee payment', 'transaction issue'],
        "question": 'Online programme fee payment me problem aa rahi hai.',
        "answer": 'Payment issues should be verified through transaction details and official payment records.'
    },
    {
        "keywords": ['online student support', 'digital help'],
        "question": 'Online programme ke liye student support kaise milega?',
        "answer": 'Online learners can access support through designated digital platforms and IGNOU student service channels.'
    },
    {
        "keywords": ['online programme completion', 'final status', 'course completion'],
        "question": 'Online programme complete hua hai ya nahi kaise check karein?',
        "answer": 'Students can verify programme completion status through their official academic records and grade card after fulfilling all required academic components.'
    },
    {
        "keywords": ['online certificate', 'digital degree', 'completion certificate'],
        "question": 'Online programme ka certificate kab milega?',
        "answer": 'Certificate issuance depends on successful completion of programme requirements and official processing schedules. Students should check latest notifications.'
    },
    {
        "keywords": ['online attendance', 'virtual class participation'],
        "question": 'Online classes me attendance kaise maintain hoti hai?',
        "answer": 'Attendance requirements for online programmes depend on programme guidelines and activities prescribed by IGNOU.'
    },
    {
        "keywords": ['online complaint', 'lms grievance', 'digital support issue'],
        "question": 'Online programme ke liye grievance kaise register karein?',
        "answer": 'Online programme learners can submit grievances through IGNOU’s official grievance mechanisms with complete details.'
    },
    {
        "keywords": ['online programme help', 'digital learning support', 'final resolution'],
        "question": 'Online programme se related final help kahan milegi?',
        "answer": 'Students should first contact the online programme support team. Unresolved issues can be escalated through SSC and grievance channels.'
    },
    {
        "keywords": ['working professional', 'job ke saath padhai', 'odl learning'],
        "question": 'Main job ke saath IGNOU se padhai kar sakta hu kya?',
        "answer": 'IGNOU’s Open and Distance Learning system is designed to support learners who wish to continue education along with employment or other responsibilities.'
    },
    {
        "keywords": ['programme selection', 'career course', 'professional learner'],
        "question": 'Working professionals ke liye kaunsa programme suitable hai?',
        "answer": 'Programme selection depends on educational qualification, career objectives and eligibility requirements of the programme.'
    },
    {
        "keywords": ['study schedule', 'working student', 'time management'],
        "question": 'Office ke saath IGNOU ki study kaise manage karein?',
        "answer": 'IGNOU provides flexible learning opportunities where students can plan their studies according to available time while completing academic requirements.'
    },
    {
        "keywords": ['counselling attendance', 'office student'],
        "question": 'Kya working professionals ko counselling attend karni hoti hai?',
        "answer": 'Counselling requirements depend on the programme structure. Students should follow instructions issued by their Study Centre and programme guidelines.'
    },
    {
        "keywords": ['missed exam', 'job problem', 'back exam'],
        "question": 'Job ke karan exam nahi de paya to kya hoga?',
        "answer": 'Students who cannot appear in an examination may appear in future examination opportunities according to IGNOU examination rules and programme validity.'
    },
    {
        "keywords": ['assignment deadline', 'working learner'],
        "question": 'Working professionals ke liye assignment submit karna difficult hai. Kya karein?',
        "answer": 'Assignments must be submitted within the prescribed schedule. Students should plan submission according to deadlines.'
    },
    {
        "keywords": ['exam preparation', 'professional student'],
        "question": 'Kya office ke saath IGNOU exam ki preparation possible hai?',
        "answer": 'Students can prepare through self-learning material, digital resources and planned study schedules.'
    },
    {
        "keywords": ['job transfer', 'centre change', 'relocation'],
        "question": 'Transfer hone par IGNOU padhai continue kaise karu?',
        "answer": 'Learners who relocate due to employment may request support regarding Regional Centre or Study Centre arrangements according to applicable guidelines.'
    },
    {
        "keywords": ['employer verification', 'course proof'],
        "question": 'Employer ko IGNOU course ke baare me information kaise milegi?',
        "answer": 'Students may provide official IGNOU admission documents, identity records and academic certificates as required by their employer.'
    },
    {
        "keywords": ['professional learner support', 'employee student'],
        "question": 'Working professional student ko special support kaise milega?',
        "answer": 'Working professionals can use IGNOU’s learner support system including Regional Centres, Study Centres, digital resources and student service channels.'
    },
    {
        "keywords": ['ignou degree validity', 'promotion', 'employer acceptance'],
        "question": 'Kya IGNOU degree job promotion ke liye valid hoti hai?',
        "answer": 'IGNOU programmes are offered through the Open and Distance Learning system. Acceptance of a qualification depends on applicable rules of employers, regulatory bodies and programme recognition requirements.'
    },
    {
        "keywords": ['admission proof', 'employment verification'],
        "question": 'Office ke liye IGNOU admission proof kaise milega?',
        "answer": 'Students can use official admission-related documents available through IGNOU systems or request guidance from the concerned student support section.'
    },
    {
        "keywords": ['skill course', 'professional development', 'certificate programme'],
        "question": 'Kya working professionals ke liye short duration skill programmes available hain?',
        "answer": 'IGNOU offers various programmes designed for different learning needs. Students should check current programme notifications and eligibility requirements.'
    },
    {
        "keywords": ['no time for classes', 'working learner support'],
        "question": 'Office ke karan Study Centre nahi ja sakta hu. Kya option hai?',
        "answer": 'Students should check programme requirements because some activities may require participation while many learning activities can be completed through self-learning resources.'
    },
    {
        "keywords": ['exam centre change', 'employee transfer'],
        "question": 'Kya working professionals ke liye exam centre change ho sakta hai?',
        "answer": 'Examination centre change requests are considered according to IGNOU examination guidelines and availability.'
    },
    {
        "keywords": ['address update', 'job relocation'],
        "question": 'Job change ke baad IGNOU records me address kaise update karein?',
        "answer": 'Students should update their contact details through the prescribed student profile update process.'
    },
    {
        "keywords": ['work experience', 'academic benefit'],
        "question": 'Kya professional experience se IGNOU me koi benefit milta hai?',
        "answer": 'Programme-specific benefits, if any, depend on approved academic rules and eligibility conditions. Students should check programme guidelines.'
    },
    {
        "keywords": ['overseas employee', 'foreign learner'],
        "question": 'Foreign country me job karte hue IGNOU continue kar sakte hain kya?',
        "answer": 'International learners and working professionals can follow applicable admission and academic procedures subject to programme availability and rules.'
    },
    {
        "keywords": ['ai assistant', 'working student help'],
        "question": 'Working professional ke liye AI chatbot se kya help mil sakti hai?',
        "answer": 'AI support can provide instant guidance regarding admission, assignments, exams, study resources and service procedures.'
    },
    {
        "keywords": ['working professional support', 'final help'],
        "question": 'Working professionals ke liye IGNOU support ka final contact kya hai?',
        "answer": 'Students should use the appropriate service channel based on their issue. Unresolved matters may be escalated through SSC and grievance mechanisms.'
    },
    {
        "keywords": ['divyang support', 'accessibility', 'special facility'],
        "question": 'Divyang students ke liye IGNOU me special facility available hai kya?',
        "answer": 'IGNOU provides learner support facilities for Divyang students according to applicable guidelines to ensure accessible and inclusive education.'
    },
    {
        "keywords": ['disability details', 'admission support'],
        "question": 'Admission ke time disability details kaise submit karein?',
        "answer": 'Students should provide disability-related information during admission or through the prescribed update process.'
    },
    {
        "keywords": ['extra time', 'scribe facility', 'exam support'],
        "question": 'Examination me extra time ya scribe facility kaise milegi?',
        "answer": 'Eligible Divyang students may request examination support facilities according to applicable examination guidelines.'
    },
    {
        "keywords": ['scribe request', 'writer facility'],
        "question": 'Scribe facility ke liye kya documents chahiye?',
        "answer": 'Required documents depend on applicable examination guidelines and verification requirements.'
    },
    {
        "keywords": ['accessible material', 'disability resources'],
        "question": 'Accessible study material kaise milega?',
        "answer": 'IGNOU provides digital and other learning resources through available platforms. Students requiring accessibility support should contact concerned support channels.'
    },
    {
        "keywords": ['accessible study centre', 'learner facility'],
        "question": 'Study Centre par Divyang students ke liye facility available hai kya?',
        "answer": 'Study Centres provide learner support according to available facilities and programme requirements.'
    },
    {
        "keywords": ['counselling support', 'disability assistance'],
        "question": 'Divyang student ke liye counselling attendance me support milega kya?',
        "answer": 'Students requiring accessibility support should coordinate with the Study Centre for suitable arrangements according to programme requirements.'
    },
    {
        "keywords": ['divyang grievance', 'accessibility complaint'],
        "question": 'Divyang student ke liye grievance kaise register karein?',
        "answer": 'Divyang learners can submit grievances related to accessibility, examination or academic support through IGNOU grievance channels.'
    },
    {
        "keywords": ['accessible lms', 'online disability support'],
        "question": 'Online learning me accessibility support kaise milega?',
        "answer": 'Online learning support depends on available digital accessibility features and platform facilities.'
    },
    {
        "keywords": ['divyang help', 'special student support'],
        "question": 'Divyang students ke liye final support kahan milega?',
        "answer": 'Divyang learners can approach Regional Centres, Study Centres and SSC for academic and service-related assistance.'
    },
    {
        "keywords": ['foreign student admission', 'overseas learner', 'international admission'],
        "question": 'Foreign students IGNOU me admission kaise le sakte hain?',
        "answer": 'International students can apply for eligible IGNOU programmes according to admission guidelines applicable to overseas learners.'
    },
    {
        "keywords": ['overseas eligibility', 'foreign learner criteria'],
        "question": 'International students ke liye eligibility kya hai?',
        "answer": 'Eligibility depends on the selected programme and academic qualifications prescribed by IGNOU.'
    },
    {
        "keywords": ['international fee payment', 'overseas payment'],
        "question": 'Foreign country se IGNOU fee payment kaise karein?',
        "answer": 'International students should use the approved payment methods and follow instructions provided for overseas learners.'
    },
    {
        "keywords": ['overseas admission confirmation', 'payment issue'],
        "question": 'Mera admission fee pay karne ke baad confirm nahi hua. Kya karu?',
        "answer": 'Students should verify payment status and submit transaction details if admission confirmation is delayed.'
    },
    {
        "keywords": ['foreign student books', 'study material abroad'],
        "question": 'Foreign students ko study material kaise milega?',
        "answer": 'Study material availability and delivery depends on programme arrangements and learner location. Digital resources may also be available.'
    },
    {
        "keywords": ['overseas online learning', 'lms access'],
        "question": 'Abroad rehkar IGNOU online classes access kar sakte hain kya?',
        "answer": 'International learners can use available digital learning platforms and online resources according to programme facilities.'
    },
    {
        "keywords": ['foreign exam', 'overseas examination'],
        "question": 'International students ka examination kaise hota hai?',
        "answer": 'Examination arrangements for international learners depend on programme guidelines and approved examination arrangements.'
    },
    {
        "keywords": ['international address update', 'contact change'],
        "question": 'Foreign address change kaise karein?',
        "answer": 'International students should update address/contact information through the prescribed process to ensure proper communication.'
    },
    {
        "keywords": ['overseas certificate', 'foreign degree delivery'],
        "question": 'IGNOU certificate foreign country me kaise milega?',
        "answer": 'Certificates are issued according to IGNOU procedures. International students should ensure correct communication details for document delivery.'
    },
    {
        "keywords": ['foreign student complaint', 'overseas grievance'],
        "question": 'International student ke liye grievance kaise register karein?',
        "answer": 'International learners can submit grievances through official IGNOU support channels with complete details.'
    },
    {
        "keywords": ['defence admission', 'army student', 'military learner'],
        "question": 'Defence personnel IGNOU me admission kaise le sakte hain?',
        "answer": 'Defence personnel can take admission in eligible IGNOU programmes by following the standard admission procedure and programme-specific eligibility requirements.'
    },
    {
        "keywords": ['defence posting', 'study continuation', 'military education'],
        "question": 'Posting ke saath IGNOU ki padhai continue kaise karein?',
        "answer": 'IGNOU’s flexible learning system supports learners who need to continue education while managing professional responsibilities and transfers.'
    },
    {
        "keywords": ['defence course', 'career programme'],
        "question": 'Defence personnel ke liye kaunsa programme suitable hai?',
        "answer": 'Programme selection depends on educational qualification, career objectives and eligibility conditions.'
    },
    {
        "keywords": ['defence transfer', 'study centre change'],
        "question": 'Transfer hone par Study Centre kaise change karein?',
        "answer": 'Defence personnel transferred to another location may request Study Centre support according to availability and applicable procedures.'
    },
    {
        "keywords": ['defence duty', 'counselling issue'],
        "question": 'Duty ke karan counselling attend nahi kar pa raha hu. Kya karein?',
        "answer": 'Counselling requirements depend on the programme. Students should contact the Study Centre for guidance regarding academic requirements.'
    },
    {
        "keywords": ['defence exam centre', 'posting change exam'],
        "question": 'Defence personnel ke liye exam centre change possible hai kya?',
        "answer": 'Examination centre change requests are considered according to IGNOU examination guidelines and availability.'
    },
    {
        "keywords": ['defence assignment', 'duty schedule'],
        "question": 'Assignment submit karne me duty ke karan problem ho rahi hai.',
        "answer": 'Assignments must be submitted within prescribed timelines. Students should plan submission according to deadlines and available support arrangements.'
    },
    {
        "keywords": ['defence study material', 'books delivery'],
        "question": 'Defence personnel ke liye study material kaise milega?',
        "answer": 'Defence learners can access IGNOU study resources through available delivery and digital learning facilities.'
    },
    {
        "keywords": ['defence verification', 'academic document'],
        "question": 'Defence service verification ke liye IGNOU document kaise milega?',
        "answer": 'Students may obtain applicable academic documents through prescribed IGNOU procedures.'
    },
    {
        "keywords": ['defence complaint', 'military learner support'],
        "question": 'Defence student ki grievance kaise solve hogi?',
        "answer": 'Defence personnel learners can use Regional Centre, SSC and grievance mechanisms for resolving academic and administrative issues.'
    },
    {
        "keywords": ['jail inmate admission', 'prison education', 'correctional education'],
        "question": 'Jail me rehne wale students IGNOU se padhai kar sakte hain kya?',
        "answer": 'IGNOU supports inclusive education initiatives and provides learning opportunities for eligible prison learners through approved channels and institutional arrangements.'
    },
    {
        "keywords": ['prison admission', 'inmate learner registration'],
        "question": 'Prison learner ke liye admission process kya hai?',
        "answer": 'Admission is processed according to IGNOU guidelines and arrangements made with authorised institutions.'
    },
    {
        "keywords": ['prison study material', 'books supply'],
        "question": 'Jail me study material kaise milega?',
        "answer": 'Study material is provided through available arrangements with concerned authorities and IGNOU support channels.'
    },
    {
        "keywords": ['prison assignment', 'inmate submission'],
        "question": 'Prison learner assignment kaise submit karega?',
        "answer": 'Assignments must be completed and submitted according to programme instructions through approved channels.'
    },
    {
        "keywords": ['prison examination', 'inmate exam centre'],
        "question": 'Jail inmates ke exam kaise hote hain?',
        "answer": 'Examination arrangements for prison learners are made according to applicable IGNOU guidelines and coordination with concerned authorities.'
    },
    {
        "keywords": ['prison counselling', 'academic support'],
        "question": 'Prison learner ko counselling facility kaise milegi?',
        "answer": 'Academic support and counselling arrangements depend on available facilities and coordination with authorised centres.'
    },
    {
        "keywords": ['prison transfer', 'record update'],
        "question": 'Jail transfer hone par IGNOU records ka kya hoga?',
        "answer": 'Students should inform the concerned authority and IGNOU support system regarding changes affecting academic communication.'
    },
    {
        "keywords": ['prison result', 'inmate grade card'],
        "question": 'Prison learner ka result kaise check hoga?',
        "answer": 'Results are processed according to IGNOU evaluation procedures and can be checked through official result systems where access is available.'
    },
    {
        "keywords": ['prison certificate', 'inmate degree'],
        "question": 'Jail inmate ko certificate kaise milega?',
        "answer": 'Certificates are issued after completion of academic requirements according to IGNOU procedures and delivered through approved arrangements.'
    },
    {
        "keywords": ['prison grievance', 'inmate support'],
        "question": 'Prison learner ki grievance kaise solve hogi?',
        "answer": 'Prison learners can raise academic and administrative concerns through authorised prison education channels and IGNOU grievance mechanisms.'
    },
]

@app.route("/")
def home():
    return "Chatbot Backend is running smoothly!"


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    if not user_message:
        return jsonify({"response": "Please type a question!"})

    # Search logic through the FAQ list
    response_text = None
    for faq in FAQS:
        if any(keyword in user_message for keyword in faq["keywords"]):
            response_text = f"\U0001F4A1 **{faq['question']}**\n\n{faq['answer']}"
            break

    if not response_text:
        response_text = "I couldn't find a matching answer. Please try asking about admission, assignments, examinations, results, certificates, study material, grievances (iGRAM), or scholarships \u2014 or rephrase your question using different keywords."
    return jsonify({"response": response_text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
