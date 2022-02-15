import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from numpy import random
from math import cos, radians
import matplotlib.pyplot as plt



def catch_all(*args,**kwargs):
    print("args=",args)
    print("kwargs=",kwargs)

def running_test():
    record = []

    c = np.ones(300,np.uint0)*180

    for x in range(200):              
        d = random.randint(180,size = 300)
        distance, path = fastdtw(d, c, dist=euclidean)
        sim = 1 - ((distance/300)/180)
        record.append(sim)

    print(np.mean(record))

if __name__ =="__main__":

    # running_test()

    # a = np.arange(300)
    # b = np.zeros(300,np.uint0)
    # c = np.ones(300,np.uint0)*180
    # d = random.randint(180,size = 300)

    fix =[]
    
    keen =[160.91989150929516, 160.73520695241095, 164.07478551751905, 165.91664577170414, 170.269368500282, 169.33700122551642, 170.14504012220434, 170.21110308406733, 170.21528141522313, 171.9633274113044, 175.46324781119674, 174.59415146604468, 176.41810139285067, 175.47555007538418, 176.33255214404997, 174.56307892198973, 171.98770093424955, 172.83959465093488, 173.66702601109176, 172.8501816992082, 171.11112972583118, 170.24949099673597, 169.3297785626224, 169.34538720990545, 171.1391358254514, 171.14457609632376, 169.35826074308082, 172.88197778108608, 171.20812073095524, 172.1538960805291, 172.09225393197832, 172.0559078908083, 171.21691488602013, 172.88050128000668, 172.86310878662817, 170.2349905081007, 170.27117831669253, 170.30963715100572, 171.29777155723406, 171.19054004928168, 170.36648250034, 171.20894060244115, 173.0580370485181, 174.6764109071499, 176.5110985273396, 179.8624338113047, 179.8147911865056, 177.41200947136454, 177.37823757496798, 176.4947662684282, 176.43787167686932, 175.6060506495597, 175.57606759913526, 170.07917878995562, 170.02503136146444, 170.89015008724925, 168.37526085648378, 171.79908807867426, 175.26550173105008, 174.37036371394052, 173.5892476309944, 172.84606115633767, 173.67906735733257, 171.10858066623777, 172.92247493327667, 172.93423079277184, 174.0120052148224, 173.85295936406771, 174.0263828047787, 173.03765127838258, 170.37742741144538, 173.0717632072854, 173.82518289457596, 173.8029513890046, 172.95042239245393, 173.5868771282967, 170.92757213565034, 163.2051243358117, 157.6607350893854, 149.84941538591943, 131.54798881679204, 122.06003404136683, 108.04764953293332, 100.45514362095184, 90.22939938111773, 84.8514349038332, 77.25903227652987, 75.25907362293924, 75.49788786346221, 77.67105909595722, 84.8358819381686, 93.69280284149903, 99.5961323672866, 115.54085145383033, 127.92276829038141, 146.0196485922738, 166.9495345412259, 165.65449423565124, 170.20666822294473, 167.7264465970542, 166.10273665559305, 167.77211391290862, 168.01228116538658, 168.11982915201315, 168.76972116214438, 168.83152269698246, 169.6480977537102, 170.59420761228532, 171.43370303449547, 172.28158569964296, 174.04185927896856, 174.08737773926273, 175.0040126179702, 174.12154149182396, 174.92187347823798, 174.20368451981972, 173.3251699470938, 168.2037223348234, 167.83756516768744, 157.68042030714656, 138.38008203759006, 125.65514086613888, 112.53613114066451, 103.13219278511184, 95.24299087304178, 87.93903160302699, 87.49749136386077, 83.56828025678715, 85.5190235665562, 86.18328220725544, 87.18677134222611, 87.02508984286231, 89.64041970148531, 89.74809561387843, 100.67643306391506, 106.10999542147593, 115.35364592235234, 127.66786698417025, 140.13280755658906, 152.2444625277556, 155.9263010287524, 162.00950799706368, 162.691614055732, 165.22983480528546, 165.3342458182704, 166.23697510684005, 165.5903670450436, 168.27391394255784, 169.89569658403423, 171.51261851344591, 171.65664946432366, 173.28408517496112, 173.2529658952749, 172.5549602321882, 174.1382627610223, 173.21425243960348, 173.34254498015844, 173.17734337648125, 173.71906419125702, 173.50842641150234, 164.67099657876264, 154.49736402564537, 142.0896267379494, 128.41428390787098, 116.62847081481428, 107.89886372681914, 97.65338353132285, 87.95622673223045, 83.22550221420659, 82.18937699787091, 83.80859160631724, 84.10752207355603, 84.77944560475567, 84.10117332058587, 90.36929442701125, 97.6085622036108, 105.10851799140062, 111.46508179088812, 128.62075823483318, 136.69814018344408, 152.6686132187303, 157.70406453958716, 168.19482796872148, 169.49583859960848, 177.18129179790816, 177.20318517924335, 178.1054457081508, 178.126508345663, 177.55476684844743, 178.30883517741827, 178.3101762418314, 178.3393239688211, 178.37497328514533, 178.35934749493498, 178.38137391043475, 178.36556724650882, 179.19815084007325, 179.17929360317714, 179.19236460526483, 177.5038111663218, 174.81480682076014, 171.17776951210737, 173.09473097726004, 159.96538109497595, 151.55391685445758, 134.96083069667657, 120.72511846708736, 110.53810114166939, 98.72140397032922, 93.25752280852913, 85.3391177512487, 84.00614038170363, 80.93441388157021, 81.63236921433116, 84.27949603865443, 87.50334726234962, 91.68555076130014, 100.96690870512356, 109.94642147576184, 121.85938387454834, 133.94499841371558, 154.20983771480059, 156.7282137627069, 160.8259617143223, 165.1328990535527, 165.9909283340329, 166.17679087836396, 167.8942127903318, 169.82042266382385, 170.79100240655796, 170.75241204646798, 172.45499401475917, 173.20601026882542, 173.2374404103406, 171.57423163765682, 172.4944214222803, 175.773743356428, 175.80096239413112, 175.665188592689, 173.94742786816175, 171.2810608943963, 171.21098444524424, 159.05261306136262, 156.0597759651652, 133.52429643979022, 121.25878402846854, 109.64315341246677, 99.97220288747314, 87.11989324731411, 84.4411396270952, 80.39434015466259, 77.84666290990947, 76.23351137432826, 78.11230691382565, 80.03842379128565, 84.861606697877, 86.86551282090738, 93.76910897803049, 102.1300196073903, 113.47278911476056, 129.492391463804, 138.40115341911502, 149.8307844065398, 156.07048488332364, 161.19789377754063, 166.91903536165265, 166.95957822778254, 167.74077229342382, 168.8905682266683, 171.3115640739395, 173.9221809484791, 177.3447249647581, 178.27859963859103, 179.91882280896252, 179.11281296287703, 178.3240043396286, 178.31271726551063, 178.26844489841608, 179.06568891488482, 177.4528404000812, 177.3371457933604, 175.68449419066027, 172.7922480707779, 170.31423416436607, 169.329246396118, 160.30273421910522, 142.2215568897478, 124.98684134629585, 115.7819087289848, 105.77070019803915, 93.72104395564884, 85.62321745812665, 82.21567118966237, 77.52884149380088, 78.23451279154881, 78.56159609747681, 78.78989120572493, 83.73996163847323, 86.73566685353956, 89.36061936945998]
    keen2=[176.00393715357302, 175.88794395517633, 175.6895966357756, 175.90805079525944, 175.53854389275193, 175.66931898137173, 174.7315393444769, 161.61184668134436, 151.18348321010114, 141.7886597786068, 126.78241296710036, 113.18294220910144, 104.68012659928286, 94.81834947089305, 85.10772614533028, 82.8537826235688, 79.53911336357277, 78.80247802142685, 78.66739767691621, 79.83280891848517, 79.89544160298544, 89.59870137986843, 95.8490422165869, 103.44163274051255, 114.4429655021938, 137.78097046347108, 153.86034621633772, 164.3918924815831, 170.52570772564255, 175.72344527518732, 172.25528945357706, 177.35830346082426, 179.66696620405355, 178.66577903620126, 178.77304143750246, 179.27482558378102, 172.25570936745916, 177.49915123974728, 173.13924596637725, 174.40066066347944, 179.87834186222864, 179.49215820518975, 178.85736530406555, 179.01553934248375, 175.281818804862, 172.26101045703817, 169.91946917423513, 174.15613427942847, 164.37142142886623, 148.56292041648058, 131.95401515205077, 119.05018271418331, 104.95073656356101, 99.38827277653945, 93.20600956182341, 87.36671131456762, 86.63087633643204, 84.26710295028784, 83.95988160614127, 82.09345568579721, 84.98953639804017, 85.61125615840547, 92.09222806021444, 99.7439082393725, 110.96200704360723, 127.42329796074907, 152.70038871644542, 164.35948176912098, 163.1344958918311, 168.04174564397704, 117.67407184384635, 174.02204470259557, 168.92108755418636, 178.77686373118271, 174.85574927491425, 179.28356022439598, 179.3438414514538, 179.82439317570504, 179.5804289681369, 179.0233881895556, 179.48880414408353, 179.6247025854885, 178.12439611742548, 176.63905621101, 176.194663302813, 177.65561609595244, 172.05869218222875, 165.96654254648928, 155.1952611637496, 141.84199319990844, 122.80555544480094, 111.39961300220361, 105.21445456544743, 98.03649704768753, 87.9910876293286, 84.45284844280667, 84.64805414489695, 82.97665348890229, 84.81457414782699, 91.03110883962381, 97.74359381330271, 105.78562001973157, 116.0611382454415, 129.9568679771919, 152.74409432500326, 167.56230831104753, 161.49962639305207, 174.9510567452923, 169.39979237671864, 172.41303814068982, 170.38513226616865, 176.0217394771339, 174.88522245892202, 178.35571959547633, 174.5716497987712, 175.77049893051856, 175.79806364184037, 177.76116355626496, 178.0160124823115, 177.41626080189414, 173.46341378631385, 171.52033623408752, 170.63285681800502, 173.03256750415116, 169.6858030333561, 168.071870564526, 158.1998272021762, 145.99389706530687, 124.52049407043455, 118.24376312554003, 112.41618979784414, 103.80347927746266, 93.89734007772671, 91.41903416471058, 91.13145702538043, 92.28978204501561, 92.0111562904575, 94.50712109544986, 96.47089955849151, 100.92806294225801, 111.87257231546178, 118.82918238950742, 131.20564943790825, 146.98071123994887, 163.87892051148006, 174.08103243031815, 178.4513024775892, 173.762350433399, 174.91122829038872, 173.01734575287549, 178.22428665671643, 178.48890651904713, 178.04762864542292, 179.71292108027885, 179.6253700825392, 178.9820875388345, 178.17058593332655, 177.84325143803426, 178.09145736092503, 177.06600559774645, 178.4695958838055, 176.77680978375042, 174.97476506449112, 176.59706737553242, 179.122102563821, 159.4893125122931, 145.97117322487165, 129.7819828764249, 120.98401843728192, 109.45282977649256, 107.5940731006718, 97.36698365703637, 96.0455560600455, 96.03312343065517, 94.28579052266764, 94.47858092163511, 93.87298412706821, 95.27005687267393, 97.62558903412594, 102.42429083759419, 110.94336485580985, 119.62138200378075, 139.60083730297055, 147.44853691899004, 160.78667843820082, 166.7580827290217, 137.4574418270392, 173.27162621230255, 169.10489123279126, 174.5267329058502, 178.2155075055467, 179.33380002981687, 179.22131499795398, 178.08394799398545, 178.36046601122368, 179.38375856444412, 179.36853029006244, 179.50563451609867, 178.59726828796764, 179.0417695211291, 174.06777130792352, 172.88089469817442, 178.4678597728204, 179.75660253283655, 165.49983323344745, 151.71933794341993, 137.84780690489967, 123.17580659561446, 116.45877190711846, 108.31578376053923, 104.80825018660315, 98.49546736670135, 93.60693745221374, 92.80756508380097, 91.99906084209067, 91.59829574447053, 94.01812304500953, 99.39809308803387, 101.7438545004348, 109.38653032464921, 121.34129994124669, 137.5721809480085, 148.4975213384941, 168.97692952990914, 171.51848329118548, 172.98274450625703, 179.7058133432919, 167.87310262453508, 171.58548890391756, 172.18582715429457, 170.31291556973167, 173.71523325500766, 171.66665947708015, 172.8886208645976, 173.19979540652272, 173.3463504684797, 178.8386165575217, 176.50110109370968, 178.5602129283523, 177.60335262739738, 172.99162620003636, 169.07949092207565, 175.07297109798674, 164.87350473021795, 148.8782961348844, 134.03295652149146, 116.31387972758873, 119.10768171110061, 109.65996943198269, 108.85475558744153, 105.87458667622852, 102.12982985831542, 103.7947735720569, 104.26209388217546, 103.05846973284116, 106.50436138175502, 109.10964712877598, 109.50181815607661, 113.64325479197012, 120.22941807276598, 138.51294136378556, 155.45152721827935, 167.65017331544982, 169.7055275632613, 175.6297593380484, 119.43160496970876, 175.12525658094532, 174.24154834096402, 178.1523897340054, 175.9182912027313, 175.64405604058254, 175.66786085258042, 175.0990659816583, 174.52014887383515, 173.7001084484763, 173.6435277834413, 174.98202036136541, 173.988556980722, 174.08001574782733, 174.19259556423776, 173.6527568130258, 173.87062970594548, 165.3030418972389, 161.83334370918104, 152.66381590220772, 139.67652351739272, 122.12976896817955, 117.6092988169687, 107.26052774506374, 105.94751692595639, 99.06622830976977, 95.50139099225203, 94.462790639221, 93.10450691619667, 92.33757292767018, 92.8632476087675, 94.65497490471273, 102.88103142483044, 104.07015901836633, 112.35628900473506]
    # c = np.ones(300,np.uint0)*np.mean(keen2)
    c = np.ones(300,np.uint0)*np.mean([50,180])
    for i in range(0,180):
        tester = np.ones(300,np.uint0)*i
        distance, path = fastdtw(tester, c, dist=euclidean)
        sim = cos(radians((distance/300)))
        sim = (sim+1)/2
        # sim = 1 - ((distance/300)/180)
        fix.append(sim)
        # sim_of_angle = cos(radians((distance/300)+40))
        # avg_distance = distance/300
        # print(avg_distance)
        # print(sim_of_angle)

    fig = plt.figure()
    # plt.plot(keen2,"-",label="raise leg")
    # plt.plot(c,"-",label="mean raise leg")
    plt.plot(fix,'-',label="fix angle")
    plt.legend()
    plt.show()

        