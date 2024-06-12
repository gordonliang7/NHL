from SalaryNN import Network as NN
from torch import load
import pandas as pd
import base64

cap_history = pd.read_csv('data/Cap History.csv').set_index('seasonId')['SALARY CAP']

sznMeans = pd.read_csv('data/Season Means.csv').set_index('seasonId')
sznSTDs = pd.read_csv('data/Season STDs.csv').set_index('seasonId')

playerIds = [8470207, 8471683, 8470058, 8470613, 8471689, 8471504, 8470176, 8471514, 8467882, 8470631, 8470065, 8471451, 8471699, 8471208, 8466371, 8474042, 8467478, 8459004, 8462060, 8470273, 8473584, 8467346, 8467519, 8471685, 8465012, 8470289, 8459433, 8451224, 8469684, 8468463, 8475158, 8472355, 8471707, 8457261, 8470169, 8468534, 8467393, 8459427, 8471388, 8471220, 8470101, 8473997, 8471671, 8471677, 8474137, 8474094, 8466035, 8470222, 8470672, 8471240, 8468846, 8474520, 8459024, 8471396, 8467371, 8470755, 8460661, 8462042, 8470697, 8459574, 8468611, 8465113, 8473459, 8473485, 8474161, 8475613, 8474571, 8469120, 8472394, 8462041, 8473999, 8465170, 8468121, 8468427, 8468095, 8470268, 8458525, 8465024, 8474567, 8474518, 8460503, 8469670, 8475381, 8464967, 8471352, 8471218, 8471748, 8471283, 8475168, 8450725, 8467875, 8458537, 8471309, 8469666, 8470225, 8455919, 8471476, 8466333, 8469544, 8470687, 8468636, 8471668, 8470804, 8474195, 8474578, 8471710, 8471729, 8464994, 8468542, 8475105, 8462036, 8468224, 8474150, 8475118, 8469459, 8473484, 8471215, 8474557, 8470136, 8471628, 8469462, 8471682, 8470750, 8460555, 8467351, 8465202, 8467502, 8470302, 8458590, 8468486, 8465050, 8473992, 8471221, 8465025, 8474563, 8462033, 8465058, 8467491, 8471280, 8470596, 8474154, 8475166, 8474565, 8459670, 8467977, 8459444, 8474250, 8474662, 8473618, 8473932, 8466378, 8471246, 8470719, 8471761, 8470085, 8470920, 8458943, 8471794, 8471895, 8475104, 8467412, 8473610, 8469473, 8471229, 8470640, 8473933, 8465026, 8468520, 8470621, 8460743, 8473682, 8470988, 8474220, 8471705, 8470615, 8462225, 8473914, 8471747, 8470301, 8467436, 8470578, 8469457, 8470274, 8475087, 8470607, 8468309, 8475098, 8470654, 8467338, 8468483, 8470609, 8471753, 8469707, 8470310, 8462129, 8471678, 8464989, 8466158, 8470383, 8473492, 8471842, 8467365, 8473466, 8467844, 8473700, 8471399, 8470614, 8472248, 8462045, 8469485, 8473526, 8474177, 8469584, 8470317, 8472370, 8467357, 8464957, 8467931, 8460502, 8473537, 8474709, 8470283, 8460621, 8467422, 8474551, 8471698, 8466142, 8470041, 8474189, 8474707, 8469755, 8470839, 8474681, 8469547, 8470828, 8473412, 8460770, 8474222, 8466139, 8471958, 8466292, 8459424, 8467545, 8470004, 8468660, 8473544, 8471409, 8471736, 8462196, 8470123, 8471236, 8471657, 8470854, 8466140, 8469472, 8470777, 8465028, 8468500, 8468626, 8470604, 8470970, 8465978, 8471282, 8471972, 8467967, 8473673, 8469506, 8474573, 8471887, 8473482, 8470774, 8470798, 8468213, 8470867, 8459514, 8473533, 8470905, 8469488, 8471346, 8471390, 8473580, 8474157, 8468001, 8469759, 8466393, 8466202, 8469476, 8471743, 8470599, 8471310, 8468535, 8471274, 8471807, 8470192, 8460527, 8468501, 8471756, 8470634, 8465210, 8460567, 8459122, 8468114, 8473510, 8471702, 8471663, 8473571, 8471810, 8466215, 8462535, 8474091, 8471273, 8460626, 8471436, 8467881, 8474184, 8471669, 8469521, 8471521, 8467361, 8459064, 8471284, 8473446, 8473546, 8466392, 8471234, 8469531, 8468577, 8472262, 8469480, 8471238, 8470741, 8473562, 8458541, 8474001, 8470699, 8468635, 8471711, 8466216, 8471879, 8471450, 8467336, 8471241, 8469638, 8470054, 8471385, 8471851, 8470996, 8466398, 8474569, 8471323, 8469500, 8460533, 8472263, 8468526, 8469820, 8469469, 8467917, 8470294, 8474102, 8460719, 8471738, 8459094, 8464966, 8470018, 8460580, 8471321, 8466300, 8470602, 8471214, 8471859, 8471804, 8475169, 8474166, 8471482, 8470662, 8473568, 8473449, 8467407, 8470329, 8471217, 8475270, 8468085, 8464979, 8474519, 8471231, 8470680, 8468598, 8474045, 8474579, 8467423, 8470724, 8471811, 8473438, 8471713, 8470047, 8471457, 8469454, 8471692, 8471419, 8474149, 8460541, 8470638, 8468789, 8470086, 8467355, 8474511, 8474552, 8468101, 8471260, 8471331, 8473534, 8471362, 8467396, 8473604, 8468674, 8470778, 8469543, 8466285, 8471365, 8470649, 8470171, 8469647, 8460492, 8473962, 8459587, 8470678, 8465056, 8465951, 8466309, 8471428, 8468083, 8469466, 8460504, 8467466, 8469575, 8471636, 8473473, 8471735, 8471269, 8467878, 8474025, 8460556, 8470617, 8470280, 8467353, 8470714, 8473600, 8474114, 8471873, 8468700, 8474576, 8459450, 8470877, 8467876, 8470230, 8462118, 8473536, 8462823, 8474046, 8471769, 8470780, 8467514, 8474564, 8470610, 8467899, 8469470, 8470543, 8469619, 8469798, 8467496, 8470896, 8470735, 8470257, 8473953, 8467915, 8462176, 8469465, 8459053, 8470636, 8471338, 8465200, 8459492, 8474153, 8459687, 8473573, 8473453, 8475174, 8473991, 8471232, 8474190, 8466181, 8466160, 8470187, 8470105, 8471741, 8466149, 8471216, 8475170, 8470611, 8471768, 8457981, 8458938, 8471733, 8466260, 8470647, 8473491, 8470729, 8470666, 8470794, 8459628, 8473493, 8474230, 8474568, 8470601, 8467329, 8470619, 8468575, 8471863, 8465185, 8471242, 8467334, 8469581, 8474574, 8471694, 8469534, 8458517, 8470834, 8474218, 8471372, 8470575, 8468208, 8458229, 8474566, 8470370, 8474138, 8471268, 8470803, 8473582, 8469460, 8473994, 8471978, 8468508, 8459462, 8474589, 8473385, 8471708, 8471312, 8474056, 8460562, 8468064, 8470180, 8464962, 8471187, 8464975, 8446053, 8459457, 8459596, 8467330, 8458951, 8470144, 8465192, 8471696, 8468639, 8458637, 8471392, 8474584, 8458519, 8470281, 8471680, 8468778, 8467331, 8470876, 8473514, 8471664, 8470131, 8459443, 8467344, 8458172, 8471265, 8467304, 8471686, 8468485, 8475172, 8475637, 8469474, 8469490, 8473924, 8469542, 8470622, 8474498, 8467370, 8471336, 8470655, 8468523, 8473550, 8468509, 8468503, 8473563, 8470162, 8468113, 8470061, 8471670, 8470606, 8471693, 8470625, 8466138, 8469639, 8470366, 8470886, 8470232, 8472215, 8473432, 8470630, 8468695, 8468510, 8473646, 8471339, 8468502, 8468707, 8460577, 8449645, 8467428, 8475086, 8471426, 8468434, 8465914, 8462038, 8445550, 8470309, 8471976, 8467408, 8470072, 8469623, 8470580, 8467332, 8469770, 8471941, 8456966, 8464956, 8474134, 8471303, 8471709, 8460720, 8471299, 8469464, 8471498, 8468704, 8468493, 8470612, 8470899, 8470740, 8459442, 8470616, 8470120, 8471311, 8465009, 8470661, 8473734, 8474040, 8470708, 8467452, 8467543, 8473419, 8459246, 8469555, 8470603, 8470713, 8470137, 8474053, 8468172, 8473542, 8468881, 8471429, 8471371, 8471261, 8468506, 8468432, 8473564, 8470299, 8473592, 8471764, 8473574, 8469455, 8466144, 8471276, 8474383, 8459640, 8470760, 8469508, 8460507, 8459547, 8468927, 8471634, 8469672, 8473898, 8469812, 8467988, 8470151, 8471290, 8469622, 8471226, 8471185, 8473525, 8470203, 8460561, 8471314, 8471681, 8467856, 8470852, 8474037, 8467389, 8471717, 8470705, 8457063, 8459461, 8467583, 8465059, 8467964, 8474291, 8471263, 8471675, 8467096, 8473712, 8468484, 8470620, 8459534, 8473548, 8470623, 8459648, 8460465, 8470318, 8471279, 8467463, 8467439, 8468513, 8470671, 8445735, 8470966, 8470104, 8471718, 8468482, 8471222, 8474125, 8470685, 8466148, 8469509, 8471766, 8466182, 8465005, 8467928, 8472382, 8473465, 8469685, 8471223, 8467579, 8467343, 8460500, 8469665, 8473496, 8466232, 8458536, 8473722, 8474141, 8468504, 8468786, 8468498, 8471266, 8469626, 8470358, 8456283, 8469598, 8473512, 8462077, 8470775, 8470600, 8468887, 8471245, 8469467, 8471676, 8472338, 8459429, 8473488, 8471704, 8471716, 8474096, 8465042, 8474674, 8467400, 8471386, 8470170, 8470039, 8466145, 8471767, 8469664, 8470153, 8475085, 8469992, 8470598, 8468517, 8470324, 8474436, 8471188, 8473504, 8459426, 8467493, 8471254, 8468518, 8470667, 8469492, 8470700, 8471703, 8467831, 8470110, 8449895, 8446485, 8470064, 8475638, 8471840, 8470063, 8467580, 8475128, 8468505, 8471233, 8470608, 8471327, 8468086, 8469483, 8470816, 8475602, 8468252, 8465122, 8474590, 8468090, 8471324, 8473687, 8471411, 8460496, 8470121, 8468162, 8472368, 8460542, 8471724, 8458529, 8470159, 8468515, 8464977, 8471697, 8471829, 8471742, 8459001, 8469779, 8464981, 8469765, 8475179, 8459454, 8468568, 8472379, 8474009, 8468478, 8470626, 8470642, 8470595, 8470644, 8469477, 8473422, 8467943, 8471483, 8456464, 8469760, 8469501, 8475167, 8470223, 8471691, 8456887, 8458361, 8473579, 8466251, 8467890, 8465166, 8474027, 8473507, 8470321, 8474535, 8474074, 8473569, 8475323, 8475372, 8470986, 8473605, 8474098, 8473589, 8474013, 8475159, 8474031, 8475990, 8473927, 8473426, 8475619, 8471956, 8475151, 8474616, 8474162, 8474673, 8473501, 8474641, 8471762, 8470737, 8474000, 8474002, 8475060, 8475641, 8458543, 8475175, 8474705, 8462093, 8467937, 8475690, 8474716, 8471474, 8473608, 8475248, 8470648, 8474164, 8473611, 8475214, 8470871, 8474731, 8469582, 8474719, 8475791, 8474100, 8474151, 8475193, 8470787, 8471368, 8474592, 8471508, 8474068, 8475186, 8474050, 8474601, 8475149, 8474192, 8471856, 8474892, 8471848, 8474030, 8470378, 8471817, 8474024, 8470265, 8475794, 8473444, 8474730, 8473913, 8467927, 8475692, 8470651, 8470201, 8471832, 8474085, 8471348, 8468599, 8471413, 8474850, 8474586, 8472410, 8474570, 8474642, 8473565, 8475788, 8474582, 8474587, 8470156, 8471714, 8471719, 8474693, 8470809, 8471786, 8474531, 8475950, 8475799, 8476208, 8474739, 8470618, 8470113, 8475150, 8475204, 8474121, 8473456, 8475603, 8475784, 8474613, 8474685, 8471490, 8475181, 8473908, 8475171, 8474727, 8474059, 8475185, 8474610, 8475640, 8475764, 8473588, 8467906, 8471730, 8469505, 8470597, 8474668, 8475160, 8474749, 8474762, 8471816, 8474609, 8464984, 8470605, 8467925, 8470656, 8458520, 8471728, 8474095, 8473970, 8475266, 8474063, 8467910, 8474048, 8471760, 8469591, 8471011, 8473560, 8474646, 8471752, 8474612, 8473558, 8474605, 8469681, 8476205, 8466212, 8474611, 8470189, 8475677, 8471862, 8475304, 8474657, 8474577, 8469564, 8473931, 8472361, 8474146, 8474038, 8474634, 8474077, 8474618, 8474207, 8475772, 8473511, 8475191, 8476466, 8471996, 8475793, 8475430, 8476381, 8474628, 8476460, 8470838, 8474581, 8475173, 8475236, 8476224, 8474691, 8474128, 8475154, 8475162, 8475650, 8448208, 8476792, 8474090, 8474168, 8475155, 8475197, 8475220, 8475268, 8475102, 8475188, 8474585, 8475455, 8471821, 8474659, 8474201, 8474604, 8476819, 8475153, 8476244, 8475233, 8474034, 8471916, 8474049, 8476459, 8475757, 8474607, 8473921, 8471701, 8475264, 8471885, 8476438, 8475148, 8475200, 8475325, 8474176, 8474625, 8475679, 8476806, 8475177, 8476206, 8475182, 8474600, 8474500, 8475183, 8473539, 8475176, 8474772, 8476455, 8474062, 8474597, 8476225, 8476457, 8474670, 8476454, 8474089, 8475758, 8476177, 8475753, 8474145, 8474666, 8468499, 8475180, 8474679, 8475283, 8472424, 8474736, 8476158, 8476116, 8475254, 8474139, 8474143, 8473867, 8475165, 8474029, 8474163, 8470005, 8475231, 8474035, 8471402, 8468584, 8469516, 8475722, 8475790, 8474575, 8474818, 8474606, 8474697, 8471846, 8475219, 8473647, 8475768, 8474631, 8476461, 8474884, 8475206, 8471868, 8471228, 8474594, 8474649, 8474774, 8474130, 8474113, 8471296, 8476211, 8475178, 8475671, 8467335, 8475225, 8470152, 8474715, 8473942, 8475218, 8475792, 8476043, 8475775, 8476799, 8475209, 8475755, 8474743, 8473616, 8476855, 8477215, 8477205, 8471262, 8476835, 8477244, 8476162, 8471853, 8474602, 8473463, 8475222, 8475598, 8475769, 8475163, 8475462, 8475745, 8471326, 8475917, 8475314, 8476539, 8474844, 8474717, 8475765, 8475164, 8476292, 8474061, 8476419, 8476870, 8475798, 8476807, 8476062, 8476888, 8476465, 8475848, 8476302, 8476887, 8474554, 8473658, 8476834, 8476482, 8474032, 8475199, 8473416, 8475761, 8476195, 8476849, 8476483, 8476467, 8471912, 8475342, 8475796, 8477243, 8475192, 8475147, 8475797, 8476872, 8474870, 8475213, 8473986, 8474661, 8475913, 8474066, 8476436, 8474744, 8475727, 8475661, 8474052, 8474849, 8474629, 8470704, 8475893, 8473944, 8475728, 8475196, 8475749, 8473911, 8474683, 8476468, 8477059, 8476463, 8474615, 8476462, 8475733, 8471700, 8475184, 8473468, 8474837, 8475395, 8476851, 8475726, 8475161, 8476456, 8475766, 8476808, 8475625, 8474688, 8475770, 8474497, 8476470, 8475958, 8474873, 8474135, 8475760, 8477082, 8477495, 8476885, 8476805, 8476850, 8475119, 8476440, 8475208, 8476941, 8477214, 8476480, 8476389, 8477501, 8476878, 8475194, 8476346, 8476427, 8474660, 8475275, 8475309, 8477847, 8474236, 8476423, 8475223, 8476879, 8475423, 8476451, 8474012, 8476304, 8477499, 8475750, 8476453, 8468745, 8477496, 8476931, 8476289, 8476442, 8476853, 8476452, 8476432, 8475759, 8475735, 8474603, 8474939, 8476854, 8476207, 8475648, 8476435, 8474005, 8475321, 8476925, 8475845, 8475567, 8475855, 8476227, 8475747, 8475754, 8477493, 8475844, 8474008, 8476430, 8475332, 8476472, 8475246, 8477289, 8477126, 8476166, 8476473, 8477492, 8475716, 8476881, 8477228, 8477227, 8477666, 8475190, 8475807, 8476209, 8476443, 8477850, 8477220, 8476411, 8477832, 8476086, 8475224, 8469752, 8475878, 8475296, 8475279, 8476179, 8476429, 8475235, 8475260, 8476975, 8477816, 8475744, 8473989, 8475815, 8475157, 8476235, 8476880, 8477290, 8476779, 8475902, 8476874, 8476191, 8475889, 8473505, 8475247, 8476367, 8476522, 8476882, 8476765, 8475739, 8477814, 8476822, 8475714, 8477507, 8476856, 8474598, 8476827, 8476871, 8476458, 8476450, 8475808, 8475198, 8475795, 8477201, 8475287, 8476410, 8475253, 8475414, 8475774, 8477836, 8477497, 8475752, 8474638, 8476445, 8475833, 8475800, 8476798, 8477448, 8476447, 8477922, 8475829, 8476336, 8476393, 8477429, 8477413, 8476147, 8476403, 8476293, 8475980, 8476439, 8475810, 8477591, 8477127, 8476363, 8476279, 8477913, 8477715, 8476384, 8475295, 8476886, 8475826, 8475842, 8477508, 8476769, 8478393, 8477902, 8476406, 8477956, 8475310, 8476549, 8476884, 8476312, 8475250, 8477455, 8476344, 8477451, 8475816, 8475907, 8477510, 8474516, 8476448, 8477933, 8476339, 8476868, 8477410, 8475294, 8473415, 8475906, 8478137, 8477887, 8477444, 8477407, 8477500, 8476477, 8475274, 8475723, 8476479, 8475715, 8476474, 8476624, 8475203, 8475996, 8474722, 8476476, 8476464, 8475243, 8478042, 8477942, 8477845, 8475767, 8476392, 8475896, 8476981, 8476469, 8475868, 8476919, 8477213, 8476437, 8476397, 8475869, 8476495, 8476386, 8477505, 8476394, 8477916, 8477932, 8476404, 8476944, 8476906, 8475763, 8477589, 8475729, 8477851, 8477498, 8476300, 8476536, 8476428, 8477494, 8476923, 8474748, 8475734, 8476921, 8476426, 8476449, 8476431, 8476967, 8474793, 8476852, 8478376, 8477070, 8477930, 8476356, 8477934, 8476478, 8476214, 8477509, 8475780, 8476989, 8472365, 8474627, 8477486, 8475732, 8477935, 8475461, 8477249, 8477566, 8477392, 8476902, 8477846, 8477463, 8477953, 8476422, 8476890, 8478928, 8477929, 8477010, 8476370, 8477464, 8478963, 8476525, 8476979, 8476368, 8477447, 8477941, 8476323, 8475730, 8477931, 8477326, 8476400, 8476955, 8477940, 8476826, 8477958, 8476545, 8476892, 8477503, 8478585, 8477433, 8478401, 8477946, 8477416, 8477997, 8477937, 8475292, 8477506, 8477955, 8477467, 8476331, 8477415, 8477426, 8478866, 8474588, 8476858, 8476915, 8475736, 8477473, 8478566, 8475762, 8476409, 8477445, 8478420, 8476905, 8478466, 8478402, 8477460, 8478004, 8476388, 8478403, 8473431, 8476200, 8477512, 8478567, 8477504, 8476471, 8476953, 8477939, 8478569, 8479293, 8478550, 8477642, 8476889, 8475832, 8477839, 8476910, 8476994, 8478373, 8475786, 8478366, 8477033, 8478564, 8477446, 8478584, 8477425, 8476934, 8476875, 8476401, 8476894, 8477406, 8475836, 8475278, 8476867, 8477018, 8475227, 8478542, 8478430, 8476288, 8477076, 8477210, 8478541, 8476869, 8477488, 8474019, 8475857, 8474698, 8477952, 8476897, 8476948, 8477901, 8476352, 8477427, 8476766, 8478563, 8476958, 8477923, 8477300, 8476913, 8476960, 8475820, 8477903, 8475738, 8478029, 8477453, 8476441, 8475949, 8477450, 8478561, 8476415, 8477527, 8477015, 8476414, 8479268, 8476917, 8475756, 8477947, 8475343, 8476326, 8477810, 8478396, 8478562, 8476379, 8476772, 8476505, 8477511, 8478528, 8477006, 8475782, 8479345, 8478906, 8478031, 8479343, 8478463, 8478495, 8478444, 8477951, 8479370, 8477502, 8476982, 8478439, 8475324, 8477491, 8479339, 8479314, 8476924, 8477466, 8479252, 8476877, 8477520, 8476418, 8477964, 8479250, 8478046, 8478480, 8476966, 8476922, 8475834, 8477034, 8477320, 8478469, 8477482, 8478512, 8477402, 8476285, 8477452, 8476891, 8477003, 8478483, 8477881, 8477950, 8476988, 8479483, 8477986, 8478500, 8475291, 8477971, 8477456, 8477458, 8476918, 8479423, 8475436, 8478073, 8477944, 8476511, 8478474, 8477479, 8477943, 8477041, 8478397, 8476399, 8478431, 8476310, 8478398, 8476374, 8479458, 8480081, 8478055, 8477462, 8478417, 8478458, 8477945, 8475982, 8477454, 8479465, 8476303, 8480087, 8479410, 8477919, 8475413, 8479648, 8478491, 8478843, 8477461, 8478010, 8478440, 8476526, 8477380, 8478131, 8477949, 8479482, 8479249, 8479318, 8477091, 8478851, 8479290, 8476873, 8477009, 8477957, 8476416, 8478400, 8479344, 8478371, 8477989, 8475210, 8478432, 8478493, 8480083, 8478460, 8479291, 8477961, 8478425, 8479969, 8478099, 8478443, 8476911, 8478506, 8476866, 8476619, 8477417, 8476857, 8478027, 8478445, 8477973, 8476219, 8477353, 8479442, 8477391, 8476425, 8477476, 8474018, 8477960, 8476390, 8477404, 8475841, 8475597, 8477346, 8477401, 8477959, 8478427, 8475263, 8476983, 8476391, 8477478, 8478414, 8477240, 8478421, 8480078, 8480015, 8477428, 8477369, 8478408, 8475718, 8478454, 8474131, 8479944, 8477337, 8478211, 8480144, 8479650, 8479325, 8479376, 8478233, 8476952, 8478075, 8478447, 8477355, 8477998, 8480113, 8480039, 8477634, 8477472, 8478451, 8477529, 8479977, 8478104, 8478846, 8478407, 8479066, 8480072, 8477969, 8477043, 8478868, 8478146, 8480009, 8479206, 8478413, 8480082, 8479407, 8477994, 8478020, 8477449, 8480158, 8479595, 8478915, 8476329, 8479974, 8479580, 8480164, 8477021, 8477046, 8478842, 8479511, 8477981, 8477471, 8479420, 8478063, 8478365, 8480761, 8478476, 8476283, 8479755, 8479398, 8475328, 8476020, 8479553, 8480727, 8479999, 8478268, 8480153, 8477474, 8480143, 8477085, 8480163, 8480029, 8477073, 8473440, 8479316, 8479337, 8476396, 8478874, 8476971, 8478462, 8479613, 8478011, 8477938, 8477987, 8477583, 8479400, 8480147, 8476617, 8477541, 8478519, 8480222, 8480330, 8478176, 8478106, 8480762, 8478873, 8480771, 8477948, 8477399, 8479404, 8479968, 8480172, 8477573, 8476372, 8480157, 8477962, 8480002, 8479366, 8478498, 8478488, 8476322, 8477359, 8479304, 8477341, 8476407, 8477936, 8480145, 8478067, 8480806, 8477972, 8480326, 8477366, 8477996, 8478911, 8478449, 8478856, 8477680, 8480074, 8478502, 8478047, 8479368, 8479657, 8479992, 8479026, 8480208, 8478136, 8480955, 8479414, 8481442, 8480944, 8480830, 8478455, 8478472, 8478841, 8479425, 8480036, 8479514, 8480821, 8477963, 8479466, 8478109, 8481186, 8481426, 8478038, 8479395, 8479320, 8480012, 8481479, 8480035, 8480341, 8480950, 8480023, 8477435, 8479346, 8480935, 8479315, 8478399, 8478409, 8480005, 8477357, 8480748, 8479447, 8479353, 8479411, 8479970, 8480948, 8479371, 8477979, 8480160, 8480776, 8480803, 8477384, 8480780, 8476907, 8480965, 8478017, 8477865, 8480314, 8479402, 8478442, 8480769, 8480901, 8479644, 8479351, 8479365, 8478881, 8480068, 8480001, 8479330, 8479333, 8480943, 8481477, 8480161, 8479336, 8480829, 8480800, 8479439, 8479372, 8480839, 8478485, 8476927, 8478416, 8480336, 8479945, 8480031, 8478891, 8478056, 8478415, 8478831, 8478468, 8480945, 8480946, 8477343, 8476278, 8478036, 8479675, 8480801, 8479385, 8478840, 8478078, 8480954, 8479324, 8477365, 8478452, 8481433, 8480073, 8479976, 8479416, 8478949, 8481481, 8481425, 8481486, 8479364, 8479388, 8478870, 8478844, 8478465, 8479415, 8479772, 8479994, 8478424, 8479393, 8479982, 8479359, 8479379, 8476947, 8480940, 8480184, 8478434, 8480021, 8479381, 8480069, 8481559, 8479382, 8478367, 8478477, 8481649, 8481105, 8481812, 8479987, 8475825, 8478882, 8478838, 8478043, 8479356, 8478859, 8479348, 8479983, 8479748, 8476987, 8481624, 8480028, 8479510, 8479933, 8481019, 8476974, 8479526, 8480018, 8479980, 8481650, 8477409, 8480043, 8477330, 8478888, 8481516, 8479587, 8480797, 8479998, 8480003, 8479571, 8478507, 8479996, 8479424, 8478996, 8478115, 8480796, 8479358, 8480064, 8480822, 8481637, 8477149, 8477974, 8480849, 8480789, 8478508, 8479369, 8480205, 8478040, 8480865, 8480185, 8479557, 8479347, 8478839, 8478058, 8480011, 8481572, 8481515, 8479523, 8478975, 8478013, 8481641, 8480186, 8480027, 8480853, 8481554, 8481600, 8479335, 8481640, 8475748, 8479542, 8480871, 8478074, 8480814, 8480913, 8477983, 8480384, 8477038, 8478857, 8478021, 8478133, 8480014, 8481638, 8479734, 8481630, 8479328, 8478436, 8481642, 8480247, 8478833, 8481523, 8479323, 8479671, 8480873, 8479985, 8481813, 8479419, 8479378, 8481533, 8480890, 8478446, 8480848, 8479547, 8480807, 8478069, 8480053, 8482222, 8482369, 8482654, 8482623, 8480037, 8480845, 8479355, 8479546, 8477314, 8480201, 8479387, 8478904, 8479661, 8480802, 8479322, 8481524, 8481147, 8481546, 8480289, 8481068, 8481058, 8481560, 8482116, 8480883, 8479718, 8478967, 8482245, 8475968, 8482248, 8478057, 8480293, 8481580, 8480467, 8480879, 8480813, 8482641, 8480196, 8482240, 8482063, 8479525, 8480844, 8480276, 8482062, 8479705, 8480063, 8481178, 8481518, 8481540, 8480056, 8480025, 8481077, 8480070, 8482142, 8478970, 8482072, 8481740, 8480221, 8481535, 8481708, 8479329, 8479573, 8477544, 8482055, 8478864, 8481599, 8480448, 8479981, 8482109, 8477335, 8482067, 8482635, 8481122, 8479986, 8479639, 8481528, 8482124, 8481629, 8480833, 8480226, 8481626, 8482241, 8480798, 8480008, 8480860, 8481014, 8479367, 8480058, 8479462, 8479984, 8479550, 8480459, 8481618, 8480817, 8481522, 8481582, 8480884, 8479602, 8481596, 8478049, 8482179, 8479516, 8478467, 8480466, 8482247, 8480831, 8481537, 8480988, 8482117, 8480041, 8481061, 8479729, 8482089, 8482665, 8481555, 8480355, 8481606, 8479536, 8482079, 8482408, 8481161, 8478486, 8481517, 8482110, 8477419, 8479578, 8483397, 8480071, 8482671, 8482070, 8481032, 8480441, 8481711, 8481133, 8481568, 8478178, 8482705, 8479520, 8480823, 8479591, 8480863, 8482113, 8481530, 8482745, 8479390, 8480980, 8482634, 8480188, 8480054, 8480847, 8481655, 8479421, 8480979, 8482624, 8480855, 8482834, 8480281, 8482192, 8479362, 8481703, 8482150, 8481441, 8480019, 8479543, 8483565, 8481815, 8479534, 8480060, 8482078, 8480434, 8481461, 8481617, 8483570, 8478147, 8482149, 8481598, 8482175, 8481093, 8477631, 8482061, 8479289, 8481849, 8481521, 8481527, 8479321, 8481489, 8480870, 8482148, 8482660, 8481239, 8481656, 8481827, 8479518, 8482073, 8482655, 8478250, 8480216, 8481657, 8482243, 8481604, 8482097, 8479991, 8482111, 8481701, 8480846, 8481557, 8479373, 8481167, 8481609, 8480842, 8479941, 8482133, 8479413, 8482667, 8481552, 8480887, 8481581, 8476345, 8479619, 8481550, 8479512, 8480192, 8480835, 8482815, 8481553, 8478062, 8480306, 8478051, 8479338, 8480443, 8479383, 8480007, 8481575, 8481720, 8481102, 8480878, 8480231, 8480220, 8481542, 8480304, 8481532, 8480292, 8478438, 8482197, 8481059, 8482475, 8482652, 8481003, 8481577, 8479972, 8479341, 8480990, 8478173, 8480049, 8482093, 8481004, 8479597, 8480259, 8482125, 8480858, 8477993, 8481592, 8482259, 8482250, 8481006, 8483597, 8482720, 8480439, 8482711, 8482452, 8482762, 8480874, 8482451, 8482679, 8480995, 8480880, 8480891, 8481704, 8480252, 8481543, 8481056, 8484287, 8481072, 8482861, 8483424, 8480246, 8482101, 8483515, 8480893, 8483808, 8480242, 8481683, 8482516, 8484256, 8481043, 8480032, 8482181, 8482730, 8481070, 8481605, 8478028, 8483619, 8482399, 8481601, 8481712, 8482712, 8482081, 8482105, 8480267, 8480034, 8481754, 8482077, 8481563, 8482684, 8481591, 8482699, 8482087, 8483620, 8480468, 8482496, 8483464, 8480245, 8480994, 8481725, 8478450, 8480328, 8483524, 8483460, 8480977, 8484254, 8482824, 8480275, 8481751, 8482159, 8479533, 8479576, 8482095, 8481690, 8480836, 8481567, 8481679, 8482207, 8478224, 8482157, 8481585, 8481013, 8482448, 8482964, 8483549, 8482146, 8481541, 8484125, 8483630, 8482740, 8480820, 8483641, 8482122, 8482176, 8482147, 8482691, 8480084, 8482092, 8481422, 8479375, 8483495, 8482074, 8481726, 8481030, 8482118, 8484258, 8483012, 8482713, 8482172, 8481789, 8482784, 8482155, 8482102, 8481716, 8481534, 8481556, 8482807, 8482809, 8482859, 8483401, 8482476, 8481699, 8484203, 8481016, 8484314, 8482787, 8479638, 8483763, 8482166, 8481719, 8481028, 8482145, 8480274, 8483512, 8483395, 8482858, 8482470, 8483468, 8482747, 8483505, 8483431, 8482765, 8483489, 8484304, 8483482, 8482511, 8483546, 8482126, 8482094, 8481024, 8484144, 8484153, 8482141, 8482744, 8484321, 8482666, 8482153, 8481564, 8484911, 8481237, 8481578, 8483490, 8483609, 8480075, 8480834, 8484166, 8480851, 8483045, 8483432, 8483398, 8482460, 8482659, 8482751, 8483471, 8484145, 8478956, 8482177, 8481593, 8482162, 8482929, 8484255, 8483491, 8483407, 8482733, 8484259, 8483457, 8483531, 8481462, 8483445, 8483920, 8482803, 8481065, 8482702, 8482088, 8483466, 8481806, 8479522, 8484149, 8478854, 8484325, 8482144, 8483567, 8483493, 8482737, 8483499, 8482749, 8481743, 8482201, 8482165, 8484326, 8481206]

indexCols = ['playerId', 'seasonId']

sumCols = ['assists', 'evGoals', 'evPoints', 'faceoffWinPct',
       'gameWinningGoals', 'gamesPlayed', 'goals', 'otGoals',
       'penaltyMinutes', 'points','pointsPerGame',
           'ppGoals', 'ppPoints','shGoals','shPoints',
           'shootingPct', 'shots', 'timeOnIcePerGame']

scoringCols = ['blockedShots', 'blocksPerGame', 'hits', 'hitsPerGame']

toiCols = ['evTimeOnIce', 'otTimeOnIce','ppTimeOnIce',
           'shTimeOnIce','shifts']

gfaCols = ['evenStrengthGoalsAgainst', 'evenStrengthGoalsFor', 'powerPlayGoalFor','shortHandedGoalsAgainst']

percCols = ['satPercentage', 'usatPercentage']

sumshootCols = ['satFor', 'satAgainst','usatAgainst', 'usatFor']

penCols = ['penalties', 'penaltiesDrawn']

queries = ['summary', 'scoringpergame', 'goalsForAgainst', 'summaryshooting', 'penalties']

forward_UFA = NN(numFeatures= 32, layers = 50)
forward_UFA.load_state_dict(load('Full Forward UFA NORMALIZED LSTM.pt'))

raw_cols = ['seasonId', 'gamesPlayed', 'goals', 'assists', 'points', 'faceoffWinPct',
            'gameWinningGoals', 'evGoals', 'evPoints', 'ppGoals', 'ppPoints', 'shGoals',
            'shPoints', 'otGoals', 'pointsPerGame', 'shots', 'shootingPct', 'timeOnIcePerGame',
            'hits', 'hitsPerGame', 'blockedShots', 'blocksPerGame', 'penaltiesDrawn', 'penalties',
            'penaltyMinutes', 'evenStrengthGoalsFor', 'evenStrengthGoalsAgainst', 'powerPlayGoalFor',
            'shortHandedGoalsAgainst', 'satFor', 'satAgainst', 'usatFor', 'usatAgainst']

nice_cols = ['Season', 'GP', 'Goals', 'Assists', 'Points', 'FOW%', 'Game-Winning Goals',
'EV Goals', 'EV Points', 'PP Goals', 'PP Points', 'SH Goals', 'SH Points',
'OT Goals', 'PPG', 'SOG', 'Shooting%', 'TOI/G', 'Hits', 'Hits/Game',
'Blocked Shots', 'Blocked Shots/Game', 'Penalties Committed', 'Penalties Drawn', 'PIM',
'EV GF', 'EV GA', 'PP GF', 'SH GA', 'Shot Attempts For', 'Shot Attempts Against',
'Unblocked Shot Attempts For', 'Unblocked Shot Attempts Against']

bad_players = [8483483, 8483652, 8482479, 8480828, 8483548, 8481576, 8482187, 8480244, 8481529, 8480840, 8483425,
               8482465, 8482673, 8480885, 8480825, 8482107, 8484274, 8480819, 8482132, 8483669, 8481525, 8482193,
               8483733, 8481614, 8482158, 8481570, 8483710, 8482918, 8483476, 8484136, 8483678, 8484268, 8482138,
               8481520, 8482484]

table_cols = [{'name': nice_col, 'id': raw_col} for raw_col, nice_col in zip(raw_cols, nice_cols)]

path_to_image = lambda x: 'data:image/png;base64,{}'.format(base64.b64encode(open(x, 'rb').read()).decode())
