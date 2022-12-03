USE cs480;

CREATE TABLE `events`(
    `event_id` INT NOT NULL AUTO_INCREMENT,
    `employee_id` VARCHAR(30) NOT NULL,
    `name` VARCHAR(300) NOT NULL,
    `location` VARCHAR(100) NOT NULL,
    `proposal_details` VARCHAR(500) NOT NULL,
    `info` VARCHAR(700) NOT NULL,
    `registration_opens_on` DATETIME NOT NULL,
    `registration_closes_on` DATETIME NOT NULL, 
    `status` VARCHAR(15) NOT NULL,
    `comments` VARCHAR(700) NOT NULL,
    `last_admin_action_by` VARCHAR(30) NOT NULL,
    PRIMARY KEY(`event_id`),
    FOREIGN KEY(`employee_id`) REFERENCES accounts(`employee_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 11 DEFAULT CHARSET = utf8; 

INSERT INTO `events` VALUES(
    1,
    '000001',
    'Doodling about biodiversity with WWF-Singapore',
    'Somerset MRT Station',
    'Proposal details',
    'Despite biodiversity’s imperative for a functioning planet, we are losing animal and plant species at an alarming rate – vertebrate populations have declined by 68% from 1970 levels according to the WWF. Join us for an interactive online workshop, where you will pick up tips from a professional artist for drawing your favorite animal, and learn about the important role of biodiversity and the threats facing our wildlife.',
    '2022-09-01 00:00:00',
    '2022-09-09 00:00:00',
    'Approved',
    '',
    ''
),(
    2,
    '000001',
    'PUB Green Run with PUB, Singapore’s National Water Agency',
    'Somerset MRT Station',
    'Proposal details',
    'Participate in the 2021 virtual edition of the PUB Green Run (formerly known as the Green Corridor Run), which is raising funds to support the rewilding of the Rail Corridor, an initiative under the National Parks Board’s ''OneMillionTrees'' movement in Singapore. For every person who participates, a portion of the registration fee will be donated to support the Nature Society (Singapore)’s rewilding effort in enhancing the ecological connectivity of the Corridor and cooling the area for recreational users.',
    '2022-09-01 00:00:00',
    '2022-09-17 00:00:00',
    'Approved',
    '',
    ''
),(
    3,
    '000002',
    'Clothing drive with Redress',
    'Somerset MRT Station',
    'Proposal details',
    'From wasting precious resources to contributing to greenhouse gas emissions, our choices have a detrimental effect on our planet. But as consumers, we can take positive steps to reduce our environmental impact. Take part in "Get Redressed Month" this October, a clothing donation campaign that aims to reduce clothing waste and encourage mindful consumption.',
    '2022-09-01 00:00:00',
    '2022-10-03 00:00:00',
    'Approved',
    '',
    ''
),(
    4,
    '000001',
    'Upcycling workshop to make face mask holders with Ground-up Initiative (GUI)',
    'Somerset MRT Station',
    'Proposal details',
    'A total of 25 participants from Singapore are welcome. Family members may also join (one Zoom login is allowed per family).

Wooden pallets are commonly used by logistics and transportation companies during delivery or shipping, often ending up in landfill. Join a hands-on online workshop to learn how to upcycle wooden pallets to create and customize sustainable holders for face masks or other everyday items. DIY kits will be provided in advance.',
    '2022-10-01 00:00:00',
    '2022-10-21 00:00:00',
    'Approved',
    '',
    ''
),(
    5,
    '000002',
    'Singapore only: Race against cancer with Singapore Cancer Society',
    'Somerset MRT Station',
    'Proposal details',
    'A total of 50 participants are needed from Singapore.

Form a Credit Suisse team and race against cancer, covering a distance of 5km, 10km, 21km or 42km over a period of nine days. A minimum donation of SGD 40 is required if you wish to participate.',
    '2022-09-01 00:00:00',
    '2022-09-17 00:00:00',
    'Pending',
    '',
    ''
),(
    6,
    '000001',
    'Teach conversational English with REACH',
    'Somerset MRT Station',
    'Proposal details',
    'A volunteer is needed from Hong Kong/Singapore to help improve students’ conversational English skills. The volunteer should be able to commit a minimum of 90 minutes once a week for a month.',
    '2022-08-01 00:00:00',
    '2022-09-01 00:00:00',
    'Pending',
    '',
    ''
),(
    7,
    '000001',
    'Hong Kong only: ICC blood donation drive with Hong Kong Red Cross',
    'Somerset MRT Station',
    'Proposal details',
    'A total of 25 volunteers are needed from Hong Kong.

With Hong Kong’s blood banks running low, the Hong Kong Red Cross is appealing for donors to participate in the upcoming blood donation drive at the ICC.',
    '2022-09-01 00:00:00',
    '2022-09-20 00:00:00',
    'Pending',
    '',
    ''
),(
    8,
    '000002',
    'LinkedIn Coaches',
    'Somerset MRT Station',
    'Proposal details',
    'Be a virtual coach to youth from Halogen Foundation. Mentors are required to have career conversations, revolving around career paths, your personal career journey, challenges and tips in job searches, etc. There will be training provided prior to the session.',
    '2022-03-01 00:00:00',
    '2022-03-17 00:00:00',
    'Pending',
    '',
    ''
),(
    9,
    '000001',
    'Write letters to the elderly with Habitat for Humanity Hong Kong',
    'Somerset MRT Station',
    'Proposal details',
    'We are looking for 20 volunteers from our Hong Kong office who are able to write in traditional Chinese.

Habitat for Humanity Hong Kong has been sending hygiene kits to their local NGO partners to support elderly care homes and social workers. Help to show the elderly that the wider community cares about them by composing a thoughtful letter or card, which will be added to each kit.',
    '2022-01-01 00:00:00',
    '2022-06-18 00:00:00',
    'Pending',
    '',
    ''

),(
    10,
    '000002',
    'Race against cancer with Singapore Cancer Society',
    'Somerset MRT Station',
    'Proposal details',
    'Form a Credit Suisse team and race against cancer. Participants can choose to cover a distance of 5km, 10km, 21km or 42km over a period of nine days. If you wish to participate in this race, we ask that you donate a minimum of SGD 60 to our selected charity, Singapore Cancer Society, regardless of the distance you have chosen to run. Participation in the event can only be confirmed upon receipt of your donation.',
    '2022-01-01 00:00:00',
    '2022-07-23 00:00:00',
    'Rejected',
    'Rejected Comments',
    ''
);