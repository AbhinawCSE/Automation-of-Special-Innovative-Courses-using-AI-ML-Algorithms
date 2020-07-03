def collegelist(nameOfTheCollege,numberOfDays,eventType):
	internationalCollegeList=["Massachusetts Institute of Technology (MIT)",
	"Stanford University",
	"Harvard University",
	"University of Oxford",
	"California Institute of Technology (Caltech)",
	"University of Cambridge",
	"University College London",
	"Imperial College London",
	"University of Chicago",
	"Princeton University",
	"University of Pennsylvania",
	"Yale University",
	"Columbia University",
	"University of Michigan,"
	"University of California Berkeley (UCB)",
	"Indian Institute of Technology Kanpur",
	"Indian Institute of Technology Bombay",
	"Indian Institute of Technology Delhi",
	"Indian Institute of Technology Madras",
	"Indian Institute of Technology Kharagpur",
	"Birla Institute of Technology and Science"]

	nationalCollegeList=["NIT Warangal (NITW)",
	"NIT Durgapur (NITDGP)",
	"NIT Surat (SVNIT)",
	"NIT Trichy (NITT)",
	"NIT Rourkela (NITRKL)",
	"National Institute of Technology Tiruchirappalli",
	"NIT Agartala (NITA)",
	"NIT Srinagar (NITSRI)",
	"NIT Delhi (NITD)",
	"Indian Statistical Institute",
	"VIT University",
	"University of Delhi",
	"Amity University",
	"Indian Institute of Technology Guwahati",
	"SRM Institute of Science and Technology",
	"Visvesvaraya Technological University",
	"Christ University",
	"PES university"]

	localCollegeList=["Ramaiah Institute of Technology",
	"Ramaiah University Of Applied Sciences",
	"BNM Institute Of Technology",
	"Dayananda Sagar College of Engineering",
	"RV College of Engineering",
	"BMS College of Engineering",
	"MVJ College of Engineering",
	"Acharya Institute of Technology",
	"New Horizon College of Engineering",
	"Cambridge Institute of Technology Bangalore",
	"RNS institute of Technology",
	"Xavier Institute of Management and Entrepreneurship",
	"Nitte Meenakshi Institute of Technology"]

	if nameOfTheCollege in internationalCollegeList and eventType=="International Event":
		if numberOfDays >=2 and numberOfDays <=5:
			return "O"
		elif numberOfDays == 1:
			return "A+"

	elif nameOfTheCollege in nationalCollegeList and eventType == "National Event":
		if numberOfDays >=2 and numberOfDays <=5:
			return "A"
		elif numberOfDays == 1:
			return "B+"
	elif nameOfTheCollege in localCollegeList and eventType == "Local Event":
		if numberOfDays >=2 and numberOfDays <=5:
			return "B"
		elif numberOfDays == 1:
			return "C+"
	else:
		return "D"

if __name__ == '__main__':
    print(collegelist(input("Enter the college name: "),int(input("Enter the number of days: "))))