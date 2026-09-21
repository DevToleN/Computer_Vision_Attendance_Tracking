![](./image1.png){width="2.7333333333333334in"
height="2.55in"}**CATHOLIC UNIVERSITY OF EASTERN AFRICA**

**PROJECT PROPOSAL FOR FINAL YEAR STUDY IN BACHELOR OF SCIENCE IN
COMPUTER SCIENCE**

**BY**

**NEVILLE KIBET 1032272**

**COMPUTER VISION ATTENDANCE TRACKING SYSTEM**

**Case Study of The Catholic University of Eastern Africa**

**DATE: April, 2025**

# **Declaration** {#declaration .unnumbered}

**This proposal is authored by Neville Kibet and is presented for the
development of a Computer Vision Attendance tracking System. In
fulfillment of the requirements for awarding of the Bachelor of Science
in Computer Science.**

# **Abstract** {#abstract .unnumbered}

**This proposal outlines the development of a Computer Vision-based
Class Attendance System aimed at resolving challenges associated with
manual attendance tracking in higher education. The system leverages
real-time facial recognition and object detection to ensure accurate and
efficient student attendance records.**

**Table of Contents**

[Declaration [3](#declaration)](#declaration)

[Abstract [3](#abstract)](#abstract)

[KEY TERMS [5](#_Toc3862)](#_Toc3862)

[Chapter 1: INTRODUCTION
[6](#chapter-1-introduction)](#chapter-1-introduction)

> [1.1 Background [6](#background)](#background)
>
> [1.2Problem Statement [6](#problem-statement)](#problem-statement)
>
> [1.3 Objectives [6](#objectives)](#objectives)
>
> [1.4 Specific Objectives
> [7](#specific-objectives)](#specific-objectives)
>
> [1.5 Justification [7](#justification)](#justification)
>
> [1.6. Scope of the Research
> [8](#scope-of-the-research)](#scope-of-the-research)
>
> [1.7 Research Organization
> [8](#research-organization)](#research-organization)

[CHAPTER 2: LITERATURE REVIEW
[9](#chapter-2-literature-review)](#chapter-2-literature-review)

> [2.1 Introduction [9](#introduction)](#introduction)
>
> [2.2 Research Methodology of Literature Review
> [9](#research-methodology-of-literature-review)](#research-methodology-of-literature-review)
>
> [2.3 History of the Research Topic
> [10](#history-of-the-research-topic)](#history-of-the-research-topic)
>
> [2.4 Review of Related Prototypes or Systems
> [10](#review-of-related-prototypes-or-systems)](#review-of-related-prototypes-or-systems)
>
> [2.5 Emerging Trends in the Research Area
> [11](#emerging-trends-in-the-research-area)](#emerging-trends-in-the-research-area)
>
> [2.6 Research Gap to be Filled
> [11](#research-gap-to-be-filled)](#research-gap-to-be-filled)
>
> [2.7Chapter Summary [12](#chapter-summary)](#chapter-summary)

[CHAPTER 3: RESEARCH METHODOLOGY
[13](#chapter-3-research-methodology)](#chapter-3-research-methodology)

> [3.1 Introduction [13](#introduction-1)](#introduction-1)
>
> [3.2 Methodology for Requirement Specification and Data Collection
> [13](#methodology-for-requirement-specification-and-data-collection)](#methodology-for-requirement-specification-and-data-collection)
>
> [3.3 Methodology for System Analysis
> [13](#methodology-for-system-analysis)](#methodology-for-system-analysis)
>
> [3.4 Methodology for System Design
> [13](#methodology-for-system-design)](#methodology-for-system-design)
>
> [3.5 Methodology for System Implementation
> [14](#section-2)](#section-2)
>
> [3.6 Methodology for System Testing
> [14](#methodology-for-system-testing)](#methodology-for-system-testing)
>
> [3.6.1White box testing [14](#white-box-testing)](#white-box-testing)
>
> [3.7 Methodology for System Deployment
> [14](#methodology-for-system-deployment)](#methodology-for-system-deployment)
>
> [3.8 Chapter Summary [14](#chapter-summary-1)](#chapter-summary-1)

[CHAPTER 4: SCHEDULE, BUDGET AND RESOURCES
[16](#chapter-4-schedule-budget-and-resources)](#chapter-4-schedule-budget-and-resources)

> [4.1 Introduction [16](#introduction-2)](#introduction-2)
>
> [4.2 Project Schedule [16](#project-schedule)](#project-schedule)
>
> [4.3 Project Budget [17](#project-budget)](#project-budget)
>
> [4.4 Project resources [17](#project-resources)](#project-resources)
>
> [4.4.1 Hardware [17](#hardware)](#hardware)
>
> [4.4.2 Software [17](#software)](#software)
>
> [4.5 Summary [17](#summary)](#summary)

[REFERENCES [18](#references)](#references)

[]{#_Toc3862 .anchor}

# **KEY TERMS** {#key-terms .unnumbered}

Facial Recognition - Biometric technology used to identify or verify a
person's identity using facial features.

SDLC - System Development Life Cycle.

# **Chapter 1: INTRODUCTION** {#chapter-1-introduction .unnumbered}

## **Background** 

Class attendance plays a critical role in monitoring student
participation, measuring academic performance, and ensuring
accountability. Traditional manual methods such as sign sheets are prone
to fraud---students often sign in for their absent peers. The rise of
computer vision and machine learning offers an opportunity to automate
this process. This project proposes a computer vision attendance system
leveraging CNNs and YOLO for real-time, accurate, and transparent
student attendance tracking.

##  {#section .unnumbered}

## **1.2Problem Statement** {#problem-statement .unnumbered}

The existing manual attendance system is inefficient, inaccurate, and
vulnerable to manipulation. There is an urgent need for an automated,
reliable, and secure solution to ensure credible attendance records
while reducing the burden on lecturers.

## **1.3 Objectives** {#objectives .unnumbered}

The general objective of this research is to design and develop a
Computer Vision Class Attendance System to automate and secure student
attendance tracking.

## **1.4 Specific Objectives** {#specific-objectives .unnumbered}

To achieve the general objective, the research will pursue the following
specific objectives:

1\. Automate student attendance using CNN and YOLO.\
2. Integrate the system with student databases for accurate records.\
3. Develop real-time reporting features for lecturers and
administrators.\
4. Evaluate system performance across varied conditions (lighting, pose,
gender, skin tone).\
5. Ensure compliance with ethical and privacy considerations.

## **1.5 Justification** {#justification .unnumbered}

The proposed research is essential for several reasons:

1\. Prevents impersonation and fraudulent attendance records.\
2. Provides real-time insights into student participation.\
3. Reduces administrative workload on lecturers.\
4. Promotes fairness by minimizing algorithmic bias.\
5. Contributes to the adoption of smart classrooms in Kenya.

## **1.6. Scope of the Research** {#scope-of-the-research .unnumbered}

The research will focus on the following aspects:

-   Geographical Scope: The study will be conducted at the Catholic
    University of Eastern Africa.

-   Technological Scope: The project will use CNN, YOLO, and OpenCV for
    face detection and recognition.

-   Time Frame: Six months, including requirement gathering, system
    design, development, testing, and evaluation.

## **1.7 Research Organization** {#research-organization .unnumbered}

The research will be organized into the following phases:

1\. Phase 1: Problem Identification and Data Collection

\- Use questionnaires to find out the shortcomings of current systems.

\- Analyze data and feedback to determine key requirements.

2\. Phase 2: Design and Development

\- Design the user interface and functionality of the system.

\- Develop the system and its website.

3\. Phase 3: Testing and Evaluation

\- Conduct a pilot study involving a sample group of students and
academic staff.

\- Evaluate the effectiveness of the system.

4\. Phase 4: Reporting and Dissemination

\- Compile the research findings into a comprehensive report.

\- Share the results through presentations.

# **CHAPTER 2: LITERATURE REVIEW** {#chapter-2-literature-review .unnumbered}

## **2.1 Introduction** {#introduction .unnumbered}

Research on automated attendance systems has grown significantly in
recent years, particularly with advances in facial recognition
technologies.

## **2.2 Research Methodology of Literature Review** {#research-methodology-of-literature-review .unnumbered}

The research methodology employed in this literature review is designed
to ensure a comprehensive understanding of the relevant body of
knowledge. The following steps have been undertaken:

1\. Database Search: Extensive searches were conducted in academic
databases such as PubMed, IEEE Xplore, Google Scholar, and relevant
journals to identify peer-reviewed articles, conference papers, and
research reports.

2\. Keyword Selection: Carefully chosen keywords and phrases were used
to retrieve relevant literature.

3\. Inclusion Criteria: Only literature directly related to facial
recognition systems and attendance tracking were included.

4\. Exclusion Criteria: Literature that did not meet the inclusion
criteria or was published before 2010 was excluded.

5\. Data Extraction and Synthesis: Key findings, methodologies, and
insights from the selected literature were extracted, summarized, and
synthesized to form the basis of this review.

**\
**

## **2.3 History of the Research Topic** {#history-of-the-research-topic .unnumbered}

The History of the use of Facial recognition in attendance tracking in a
university context can be separated into different phases:

1\. Early Experiments: Universities first began exploring biometric
attendance systems in the early 2000s as alternatives to manual roll
calls and RFID-based ID cards. Fingerprint scanners and swipe cards were
among the earliest technologies, but they presented issues such as
hygiene concerns, system failures, and the possibility of students
marking attendance for others.

2\. Rise of Computer Vision and Machine Learning: With the emergence of
open-source libraries like OpenCV and the growing success of deep
learning--based face recognition algorithms, institutions started to
experiment with facial recognition as a more reliable, contactless
solution. Pilot projects emerged in Asia, Europe, and North America,
where lecture halls installed cameras to automatically identify students
during lectures without disrupting class.

3\. Integration and Expansion: As the technology matured, facial
recognition systems were integrated with university databases and
student information systems. This allowed real-time attendance tracking
across multiple classrooms, automatic report generation, and connections
to broader academic performance analytics. Administrators and lecturers
could monitor student engagement more efficiently, reducing paperwork
and human error.

4\. Privacy and Ethical Considerations: The rise of facial recognition
raised important questions around privacy, security, and consent.
Universities had to navigate regulations such as the General Data
Protection Regulation (GDPR) in Europe and the Family Educational Rights
and Privacy Act (FERPA) in the United States. These concerns influenced
how data was stored, processed, and accessed.

5\. Modern Adoption and Smart Campus Initiatives: Today, facial
recognition attendance systems are part of broader smart campus
strategies that combine artificial intelligence, Internet of Things
(IoT) devices, and advanced analytics. These systems not only streamline
attendance but also enhance overall academic administration and
contribute to creating data-driven environments that support teaching,
learning, and campus management.

## **2.4 Review of Related Prototypes or Systems** {#review-of-related-prototypes-or-systems .unnumbered}

1\. Early Camera-Based Recognition Systems:

The first attempts at using facial recognition in universities relied on
standard CCTV cameras combined with basic image processing techniques.
These systems were often experimental and had limited accuracy, as they
struggled with varying lighting conditions, different facial
orientations, and image quality. They provided proof of concept but
lacked the robustness needed for real-world university deployment.

2\. OpenCV-Based Attendance Systems:

With the development of the OpenCV library, many institutions and
researchers began experimenting with real-time face detection and
recognition. OpenCV's Haar cascades and later its deep learning--based
detectors allowed faster and more accurate recognition in classroom
environments. These systems enabled live attendance logging through
webcams, making them affordable and relatively easy to implement.
However, their accuracy was often affected by background noise, changes
in student appearance, and limited ability to distinguish between
identical twins or very similar-looking students.

3\. FaceNet and DeepFace Implementations:

Advanced deep learning models like Google's FaceNet and Facebook's
DeepFace significantly improved recognition accuracy by extracting
highly distinctive facial embeddings. Universities that piloted systems
based on these models achieved more reliable student identification even
under varying conditions. Such systems were often integrated with
student databases, enabling automated reporting and reducing manual
intervention. The challenge, however, was the need for high
computational resources and the requirement to maintain large datasets
for training and testing.

4\. Commercial Facial Recognition Platforms:

Several commercial solutions such as Microsoft Azure Face API, Amazon
Rekognition, and Face++ have been adopted by universities seeking
cloud-based scalability. These platforms provide pre-trained models with
high accuracy and support large-scale deployments across multiple
campuses. Their advantages include real-time recognition, integration
with mobile apps, and data analytics capabilities. However, reliance on
cloud services raises concerns about cost, data privacy, and compliance
with local data protection regulations.

5\. Hybrid Systems with IoT Integration:

Some modern attendance tracking systems combine facial recognition with
IoT devices, such as smart cameras, RFID sensors, and edge-computing
devices. These hybrid systems capture and process facial data locally
before syncing with central databases, reducing latency and improving
security. They are part of broader smart campus initiatives, enabling
not only attendance tracking but also classroom monitoring, access
control, and predictive analytics.

6\. Mask-Resilient and Post-COVID Systems:

In response to the COVID-19 pandemic, universities explored facial
recognition systems capable of identifying students wearing masks.
Techniques such as partial face recognition and infrared-based detection
have been integrated into newer systems to maintain accuracy while
adhering to health protocols. These innovations highlight the
adaptability of facial recognition systems to changing environments and
societal needs.

##  {#section-1 .unnumbered}

## **2.5 Emerging Trends in the Research Area** {#emerging-trends-in-the-research-area .unnumbered}

As Facial Recognition technology continues to evolve, several emerging
trends have become evident:

-   Integration with Artificial Intelligence and Deep Learning:

Modern facial recognition systems in universities are increasingly
powered by advanced AI models, such as convolutional neural networks
(CNNs) and transformer-based architectures. These models enhance
recognition accuracy, even under challenging conditions like poor
lighting, partial occlusion, or changes in appearance. Transfer learning
and pre-trained models like FaceNet, ArcFace, and VGGFace are being
widely adopted to reduce training costs and improve performance.

-   Edge Computing and On-Device Processing:

To address concerns about latency, bandwidth, and data security,
universities are adopting edge-based solutions where facial data is
processed locally on IoT-enabled cameras or dedicated devices. This
reduces the need to transmit sensitive information to centralized
servers or cloud platforms, ensuring faster real-time recognition and
better compliance with privacy regulations.

-   Cloud-Enabled Smart Campus Solutions:

Cloud computing platforms such as Microsoft Azure Face API, Amazon
Rekognition, and Google Cloud Vision are being integrated with
university systems for scalability and centralized management.
Cloud-based attendance tracking allows seamless synchronization across
multiple campuses, supports large-scale data analytics, and enables
integration with student information systems for automated reporting.

-   Contactless Authentication Post-COVID:

The COVID-19 pandemic accelerated demand for contactless attendance
solutions. Emerging systems are now optimized for recognizing students
wearing face masks, using partial face recognition and thermal imaging
for enhanced accuracy. Universities are prioritizing systems that
balance health protocols with efficiency in attendance management.

-   Privacy-Preserving Techniques:

With growing concerns around surveillance and student data protection,
emerging systems are adopting privacy-preserving technologies such as
federated learning, homomorphic encryption, and differential privacy.
These methods ensure that facial recognition models can be trained and
deployed without exposing sensitive biometric data, aligning with
regulations like GDPR and FERPA.

-   Multimodal Biometric Systems:

To increase reliability, universities are exploring multimodal systems
that combine facial recognition with other biometric methods such as
voice recognition, gait analysis, or iris scanning. These hybrid
solutions minimize false positives and provide redundancy, ensuring
higher accuracy in high-stakes environments such as examinations and
secure facility access.

-   Predictive Analytics and Student Engagement Monitoring:

Emerging systems are not limited to attendance tracking but are being
linked to predictive analytics dashboards. By combining attendance
records with academic performance data, universities can identify
at-risk students, monitor engagement trends, and implement early
intervention strategies. This trend reflects a shift toward using facial
recognition as part of broader learning analytics frameworks.

-   AI Ethics and Regulatory Compliance:

As facial recognition becomes more prevalent, there is growing emphasis
on ethical AI frameworks, transparency, and responsible data usage.
Universities are adopting governance models that involve informed
consent, clear data retention policies, and regular audits to ensure
compliance with evolving national and international data protection
laws.

## **2.6 Research Gap to be Filled** {#research-gap-to-be-filled .unnumbered}

Although facial recognition systems have advanced in university
attendance tracking, several gaps remain. Current solutions often
struggle with accuracy in real-world conditions such as poor lighting,
occlusions, and large classroom settings, limiting scalability. Most
systems are focused solely on attendance logging, leaving a gap in
integration with broader academic analytics for monitoring engagement
and performance. Additionally, there is insufficient attention to
privacy, data security, and ethical concerns, particularly around
compliance with regulations like GDPR and FERPA. Finally, research on
affordable, resource-efficient solutions suited for universities in
developing regions remains limited.

## **2.7Chapter Summary** {#chapter-summary .unnumbered}

This review of related works has provided an in-depth understanding of
the research topic, starting from its historical context to the current
state of the field. It highlighted existing prototypes and systems
developed. Additionally, the review identified emerging trends in the
research area, such as AI Ethics and integration, which are shaping the
future of the industry.

Most importantly, this review emphasized the research gap that this
study seeks to fill -- the development of a Computer Vision Class
Attendance System solution to ensure credible attendance records while
reducing the burden on lecturers. This gap forms the basis for the
research objectives outlined in this study\'s proposal.

# **CHAPTER 3: RESEARCH METHODOLOGY** {#chapter-3-research-methodology .unnumbered}

## **Introduction**

The project methodology that we will use in the development of the
android application is the System Development Life Cycle (SDLC). The
SDLC is the process of understanding how information system can be valid
to the user needs, then designing the system, building it and delivering
it to the potential users. This methodology is composed of some phases.
The structured design methodology will be waterfall development.

## **3.2 Methodology for Requirement Specification and Data Collection** {#methodology-for-requirement-specification-and-data-collection .unnumbered}

1\. Data Sources

To specify the requirements for the attendance system, we will gather
data from multiple sources:

\- Surveys: Structured questionnaires will be distributed to university
students and lecturers to understand their needs and challenges.

\- Interviews: In-depth interviews will be conducted with a subset of
lecturers and university staff to gain qualitative insights.

\- Existing Data: We will collect data from the manual student
attendance records.

2\. Data Analysis

Both qualitative and quantitative data will be analyzed. Qualitative
data will be subjected to thematic analysis to identify key
requirements. Quantitative data will be analyzed using statistical
methods to determine patterns and preferences.

## **3.3 Methodology for System Analysis** {#methodology-for-system-analysis .unnumbered}

The proposed information system will use Object oriented analysis and
Design (OOAD) approach. OOAD is an analysis approach that that uses
object-oriented techniques to 9 manipulate, analyze and improve the
quality of the information system being developed

1\. Workflow Analysis

The existing workflow of current manual and biometric attendance systems
will be analyzed to identify bottlenecks, inefficiencies, and areas for
improvement.

2\. User Input

User Input from existing systems will be developed based on the
requirements collected, providing a clear understanding of what the
system should deliver from the users\' perspective.

## **3.4 Methodology for System Design** {#methodology-for-system-design .unnumbered}

1\. Prototyping

I will create wire-frames and prototypes to visualize the application\'s
user interface and features. Feedback from potential users will be
incorporated into the design.

2\. Architecture Design

The system architecture will be designed to ensure scalability,
security, and performance. Decisions regarding databases, frameworks,
and technology stacks will be made.

![](./image2.png){width="6.5in" height="2.716666666666667in"}

Image 1 ERD

## ![](./image3.png){width="6.5in" height="6.110416666666667in"} {#section-2 .unnumbered}

Image 2:Data flow

## **3.5 Methodology for System Implementation** {#methodology-for-system-implementation .unnumbered}

1\. Python

Python is the core programming language used to build the system. Its
simplicity and extensive ecosystem make it ideal for developing
applications that integrate machine learning, computer vision, and
databases. In this project, Python acts as the glue that ties all the
components together: it runs the Flask web application, handles
communication with the MySQL database, manages image preprocessing, and
calls the machine learning models for face recognition.

2\. OpenCV

OpenCV (Open Source Computer Vision Library) is used for image capture
and preprocessing. It connects to webcams or IP cameras, detects faces
in real time, crops and normalizes them, and prepares them for further
analysis by TensorFlow. In this project, OpenCV is responsible for the
frontline visual processing, such as detecting student faces from the
classroom feed and passing them to the recognition model. It also
provides visualization tools to display attendance feedback (e.g.,
showing a student's name on the screen when recognized).

3\. MySQL

MySQL serves as the database system for storing and managing data. It
maintains records of students, their facial encodings, attendance logs,
courses, and administrator accounts. When a student is recognized by the
system, MySQL stores the event with details like student ID, course,
timestamp, and camera source. It ensures data consistency, allows
administrators to generate attendance reports, and integrates with
existing university information systems.

4\. TensorFlow

TensorFlow is the machine learning framework used to handle facial
recognition. It powers the neural network models that convert a
student's face into a numerical representation (embedding), which is
then compared to stored embeddings in the database. TensorFlow ensures
that recognition is accurate and efficient, even under varying
conditions such as changes in lighting or student appearance. In this
project, it is the intelligence layer that determines whether a captured
face matches a registered student, enabling reliable attendance marking.

## **3.6 Methodology for System Testing** {#methodology-for-system-testing .unnumbered}

## **3.6.1White box testing** {#white-box-testing .unnumbered}

The proposed system proposes to use white box testing as a testing
method. This type of testing involves having test cases derived from
information on the source code. White box testing is appropriate in this
case because the tests will be done by the proposed system developer,
who has written the code and knows what to expect from the written code.

## **3.7 Methodology for System Deployment** {#methodology-for-system-deployment .unnumbered}

1\. Beta Testing

The application will be released in a controlled beta environment to
gather feedback and identify any last-minute issues.

2\. Production Deployment

After successful beta testing, the application will be deployed to the
production environment, making it available to lecturers and system
administrators.

## **3.8 Chapter Summary** {#chapter-summary-1 .unnumbered}

This research methodology chapter has outlined the strategies and
methods that will be employed in each phase of the project. The
requirement specification and data collection phase will involve
surveys, interviews, and data analysis to identify further system needs.
System analysis will examine workflow and create user stories. The
system design will include prototyping and architectural planning.
System implementation will focus on coding and continuous integration.
System testing will encompass various scenarios and user testing.
Finally, system deployment will begin with beta testing and culminate in
a full production release.

By following this comprehensive methodology, this research aims to
develop an automated, reliable, and secure solution to ensure credible
attendance records while reducing the burden on lecturers.

# **CHAPTER 4: SCHEDULE, BUDGET AND RESOURCES** {#chapter-4-schedule-budget-and-resources .unnumbered}

##  {#section-3 .unnumbered}

## **4.1 Introduction** {#introduction-2 .unnumbered}

The schedule, budget and resources are components necessary for the
execution of the project.

Project schedule determines the timeline for developing the system,
including key milestones and deadlines to ensure systematic progress.
The budget covers financial aspects including costs for technology,
software, to prevent cost overruns and ensure resource availability.

These elements provide a foundation for effective project management
enabling progress tracking, risk management and informed decision making
throughout the project.

## **4.2 Project Schedule** {#project-schedule .unnumbered}

Figure 1:GanttChart

![](./image4.png){width="6.5in" height="3.1798611111111112in"}

**\
**

## **4.3 Project Budget** {#project-budget .unnumbered}

  -----------------------------------------------------------------------
  **Resources**           **Quantity**            **Cost(KSH)**
  ----------------------- ----------------------- -----------------------
  **Computer**            **1**                   **54,000**

  **Camera Equipment**    **1**                   **20,000**

  **Internet**                                    **6,000**

  **Python**                                      **Free**

  **TensorFlow**                                  **Free**

  **MySQL**                                       **Free**

  **Total**                                       **80,000**
  -----------------------------------------------------------------------

  : Table 1: Budget

###  {#section-4 .unnumbered}

## **4.4 Project resources** {#project-resources .unnumbered}

### 4.4.1 Hardware {#hardware .unnumbered}

1\. Camera Equipment.

2\. Computer (Laptops or desktops).

3.Internet connection.

### 4.4.2 Software {#software .unnumbered}

1.Python.

2.TensorFlow.

3.OpenCV.

4\. MySQL.

## **4.5 Summary** {#summary .unnumbered}

In conclusion, this proposal outlines a structured approach to
developing a Computer Vision Class Attendance System to automate and
secure student attendance tracking. By addressing the identified
challenges and leveraging data driven insights, the proposed application
has the potential to significantly improve real-time, accurate, and
transparent student attendance tracking.

# **REFERENCES** {#references .unnumbered}

1\. Budiman, A. (2023). CNN vs LBPH for Student Attendance. Procedia
Computer Science.\
2. Banerjee, P. (2024). Automated Attendance Generation in Real Time
Using Computer Vision. ResearchGate.\
3. Boe, R. (2024). Real-Time Student Attendance with HOG and CNN. JOIV
International Journal.\
4. Nguyen-Tat, T., et al. (2024). Haar Cascade Attendance System on
Jetson Nano. arXiv.\
5. Rao, S. (2022). AttenFace: A Scalable Real-Time Attendance System.
arXiv.\
6. Redmon, J., & Farhadi, A. (2018). YOLOv3: An Incremental Improvement.
arXiv.\
7. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning.
MIT Press.
