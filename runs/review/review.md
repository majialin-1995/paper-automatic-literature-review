# 文献综述整理草稿（按大类/小类分组)


## 轴承故障诊断的深度特征学习方法


### 多尺度与多域特征提取

“多尺度与多域特征提取”这一小类主要汇总了 6 篇相关工作，时间范围集中在 2025 年左右。

- 章伟忠等人{基于改进卷积神经网络的滚动轴承故障诊断方法研究}针对滚动轴承在强噪声、单源信息不足和样本稀少工况下故障诊断精度低的问题，提出基于改进卷积神经网络（如参数优化辛几何模式分解、多传感器数据融合和动态全局适应注意力机制）的系列诊断方法，显著提升了模型的抗噪声能力、特征提取能力和小样本诊断精度，增强了故障诊断的鲁棒性和实用性。
- 谢睿等人{基于深度学习的轴承故障诊断与剩余寿命预测方法研究及应用平台开发}针对轴承故障诊断中样本不均衡导致精度低、剩余寿命预测中健康指标构建困难及结果可信度不足的问题，提出基于扩散模型和双焦点损失CNN的诊断方法以及结合分位数回归与特征融合的预测方法，并开发了集成这些技术的工程化平台，显著提升了诊断准确性和预测可靠性。
- 胡怡帆等人{基于深度学习的滚动轴承故障诊断与剩余寿命预测研究}针对滚动轴承故障诊断中特征提取不充分、剩余寿命预测中退化过程表征不足和预测精度低的问题，提出基于双通道特征提取、多尺度残差卷积自编码器及双向门控循环单元与自注意力机制相结合的方法，有效提高了故障诊断准确率和剩余寿命预测精度。
- 毋毓斌等人{基于概率度量与高斯混合模型的轴承故障诊断方法}针对轴承故障数据维度高、特征复杂导致传统智能算法分类效果不佳的问题，提出结合高斯混合模型与概率度量的局部线性嵌入优化方法，通过融合全局与局部特征提取及改进距离度量，显著提升了故障诊断准确率至95%以上。
- Lei Fu;Zepeng Ma;Libin Zhang;Dapeng Tan等人{Cross layer-scale fault diagnosis with unsupervised criteria for maximizing information and minimizing redundancy}针对现有轴承故障诊断方法难以同时捕捉局部脉冲特征、表征冲击性和循环平稳性、以及完整提取故障分量的问题，提出跨层尺度重构方案，通过自适应斜率边缘滤波器和无监督准则最大化信息并最小化冗余，显著提升了故障检测的准确性和完整性。
- 陈莹洁等人{基于深度学习的滚动轴承故障诊断系统研究与实现}针对工业环境中滚动轴承因强噪声干扰和跨工况差异导致的故障诊断难题，提出基于多尺度特征融合和深度迁移学习的智能诊断方法，并开发了在线监测工具，显著提高了诊断准确率和可靠性，为工业设备维护提供了高效智能的解决方案。

综合来看，“多尺度与多域特征提取”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 章伟忠、谢睿、胡怡帆 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 注意力机制与时序建模

“注意力机制与时序建模”这一小类主要汇总了 1 篇相关工作，时间范围集中在 2025 年左右。

- 麻全;艾绍腾;张泽阳;刘东;徐卓飞等人{基于连续小波分析与注意力机制的滚动轴承故障诊断}针对滚动轴承故障诊断中深度学习模型可解释性差、过程不清晰的问题，提出基于连续小波分析与压缩激励注意力机制的卷积神经网络方法，通过可视化解释故障频谱规律，将诊断准确率提升至98.81%，显著增强了模型的可解释性。

综合来看，“注意力机制与时序建模”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 麻全;艾绍腾;张泽阳;刘东;徐卓飞 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 轻量化与噪声鲁棒特征学习

“轻量化与噪声鲁棒特征学习”这一小类主要汇总了 3 篇相关工作，时间范围集中在 2025 年左右。

- 李璐等人{基于深度学习技术的内燃机车发动机轴承故障诊断方法}针对内燃机车轴承故障诊断中噪声干扰强、工况适应性差和检测效率低的问题，提出融合自适应信号处理与深度学习的智能诊断方法，通过优化振动信号采集和构建轻量化神经网络，显著提升了混合噪声抑制与多转速域泛化能力，为铁路机务段检修提供了可靠技术支撑。
- 秦毅;杨瑞;赵丽娟;毛永芳等人{面向轴承故障诊断的无监督噪声自适应匹配追踪算法展开去噪网络}针对轴承振动信号噪声干扰导致故障诊断精度受限的问题，提出一种基于DCT-Laplace字典和小波变换噪声估计的无监督噪声自适应匹配追踪算法展开去噪网络，通过自适应确定展开数以去除噪声并保留故障特征，显著提升了噪声环境下的诊断精度。
- 朱天伦等人{基于对抗蒸馏与Hessian矩阵的轻量级轴承故障诊断方法}针对传统轴承故障诊断技术效率低、深度学习模型计算成本高且难以实时应用的问题，提出了基于对抗蒸馏与均匀量化的轻量级方法（UQAD）和基于Hessian矩阵的自动量化感知训练方法（HAQAT），通过降低模型复杂度、提升鲁棒性和自动优化量化精度，显著实现了在资源受限设备上高效、准确的跨域故障诊断。

综合来看，“轻量化与噪声鲁棒特征学习”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 李璐、秦毅;杨瑞;赵丽娟;毛永芳、朱天伦 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


## 跨工况与跨设备的域自适应诊断


### 统计分布对齐方法（MMD/LMMD/子域对齐）

“统计分布对齐方法（MMD/LMMD/子域对齐）”这一小类主要汇总了 30 篇相关工作，时间范围大致覆盖 2023–2025 年。

- Shouqiang Kang;Yulin Sun;Xinrui Li;Yujing Wang;Qingyan Wang;Xintao Liang等人{Unsupervised fault diagnosis method for rolling bearings based on federated universal domain adaptation}针对滚动轴承私有数据不共享、分布差异及标签空间差异导致诊断精度低的问题，提出基于联邦通用域适应的无监督故障诊断方法，通过随机映射、混合径向基核最大均值差异和边界向量实现特征对齐与未知类分离，显著提升了跨客户端的诊断准确率。
- 崔朝阳;杨绍普;顾晓辉;申永军等人{基于多层联合分布自适应的高速列车轴箱轴承故障诊断方法}针对数据驱动故障诊断模型依赖大量标记数据且要求训练与测试数据独立同分布的问题，提出基于多层联合分布自适应的一维卷积神经网络方法，通过减小源域与目标域在边缘和条件分布上的差异，实现了跨工况高速列车轴箱轴承的无监督智能诊断，显著提升了迁移诊断性能。
- Xiaoxu Li;Jiahao Wang;Jianqiang Wang;Jixuan Wang;Qinghua Li;Xuelian Yu;Jiaming Chen等人{Research on Unsupervised Domain Adaptive Bearing Fault Diagnosis Method Based on Migration Learning Using MSACNN-IJMMD-DANN}针对变工况下轴承故障诊断中特征提取困难、标记样本获取成本高以及域分布差异大的问题，提出基于迁移学习的MSACNN-IJMMD-DANN无监督域自适应方法，通过多尺度注意力机制、改进的联合最大均值差异和域对抗网络显著提升了跨域诊断性能。
- Bin Liu;Changfeng Yan;Chao He;Ming Lv;Jianxiong Wei;Lixiao Wu等人{An interpretable physics-informed subdomain moment-enhanced adaptation network for unsupervised transfer fault diagnosis of rolling bearing}针对滚动轴承故障诊断中数据依赖性强、缺乏可解释性及跨域特征差异大的问题，提出基于物理信息动态卷积和高阶矩度量的可解释子域自适应网络，通过物理核映射与子域对齐显著提升了跨工况诊断的准确性与可解释性。
- 欧阳炳等人{基于领域自适应的宽度学习滚动轴承故障诊断方法研究}针对滚动轴承故障诊断中特征冗余、参数敏感和跨域泛化弱的问题，提出融合领域自适应与宽度学习的轻量化框架，通过特征选择-参数优化-领域迁移协同机制，在提升诊断准确率的同时显著降低计算成本。
- 周圆等人{基于深度迁移学习的滚动轴承故障诊断方法研究}针对滚动轴承故障诊断中传统深度学习方法依赖大量标记数据且难以处理多尺度特征差异的问题，提出基于纹理损失与核范数正则化的特征增强迁移学习模型，通过多尺度特征对齐和低秩近似提取有效特征，显著提高了诊断精度和鲁棒性。
- 李豪等人{基于联邦学习的轴承故障诊断研究}针对轴承故障诊断中数据隐私保护、样本稀缺、非独立同分布等挑战，提出基于联邦学习的自适应聚合、动态聚类和去中心化改进方法，显著提升了诊断准确性、安全性和变工况适应能力。
- 张旭阳等人{基于迁移学习的轮对轴承故障诊断方法研究}针对轮对轴承故障数据稀缺且跨场景诊断模型泛化能力不足的问题，提出基于迁移学习的域适应和域泛化方法，通过动态对抗联合域适应和因果分解机制提升模型鲁棒性，并开发智能诊断系统，显著提高了故障诊断的准确性和运维效率。
- Qi Chang;Congcong Fang;Wei Zhou;Xianghui Meng等人{A multi-order moment matching-based unsupervised domain adaptation with application to cross-working condition fault diagnosis of rolling bearings}针对滚动轴承故障诊断中因领域漂移导致目标域样本易被误分类的问题，提出一种基于多阶矩匹配的无监督领域自适应方法，通过低阶与高阶矩匹配实现粗细粒度混合对齐，并结合判别性聚类提取领域不变特征，显著减少了负迁移现象。
- 吕智明等人{基于深度域适应的滚动轴承故障诊断方法研究}针对滚动轴承在复杂多变工况下故障诊断时面临的数据分布差异、目标域无标签及模型泛化能力不足的问题，提出基于深度域适应的跨工况诊断方法和多源域泛化的未知工况诊断方法，显著提升了模型在不同场景下的诊断准确率和鲁棒性，为设备高可靠运行提供了有效解决方案。
- 谭海冰等人{基于改进的多尺度残差网络与迁移学习的轴承故障诊断研究}针对滚动轴承传统故障诊断方法繁琐低效、信号易受噪声干扰、跨工况和设备诊断性能退化等问题，提出基于改进多尺度残差网络与迁移学习的方法，通过信号图像化、空洞卷积与可变形卷积增强特征提取，并结合LMMD和对抗迁移学习实现跨工况/设备知识迁移，显著提升了诊断准确性、抗噪性和泛化能力。
- 刘贵毅等人{变转速工况下滚动轴承故障诊断方法研究}针对变转速工况下滚动轴承故障特征难以提取、传统诊断方法失效的问题，提出结合阶次分析和短时傅里叶变换的方法，并构建轻量化深度学习框架与跨域迁移学习网络，显著提升了诊断的准确性、鲁棒性和泛化能力。
- Shuping Wu;Peiming Shi;Xuefang Xu;Xu Yang;Ruixiong Li;Zijian Qiao等人{KMDSAN: A novel method for cross-domain and unsupervised bearing fault diagnosis}针对无标签数据集导致的跨域轴承故障诊断难题，提出基于K-means聚类优化子域对齐的非对抗网络方法KMDSAN，通过改进注意力机制和局部最大均值差异优化，显著提升了跨域诊断准确率。
- Hao Luo;Xinyue Wang;Li Zhang等人{Normalization-Guided and Gradient-Weighted Unsupervised Domain Adaptation Network for Transfer Diagnosis of Rolling Bearing Faults Under Class Imbalance}针对滚动轴承故障诊断中类别不平衡导致少数类分类边界学习困难的问题，提出一种基于归一化引导和梯度加权的无监督域自适应网络（NG-UDAN），通过域归一化模块和梯度加权焦点损失有效解决了跨域特征偏移与域内类别不平衡的挑战。
- Feng Xiaoliang;Zhang Zhiwei;Zhao Aiming等人{Unsupervised domain adaptation bearing fault diagnosis method based on joint feature alignment}针对轴承在不同工况下数据分布差异导致深度学习模型跨条件故障诊断效果不佳的问题，提出基于联合特征对齐的无监督域适应方法，通过多层多带宽柯西核最大均值差异和互信息综合对齐源域与目标域的边际与条件分布，显著提升了模型在未标记目标域上的诊断性能。
- Bin Liu;Changfeng Yan;Yaofeng Liu;Ming Lv;Yuan Huang;Lixiao Wu等人{ISEANet: An interpretable subdomain enhanced adaptive network for unsupervised cross-domain fault diagnosis of rolling bearing}针对噪声干扰下全局域适应忽略子域分布导致多类别局部差异的问题，提出可解释子域增强自适应网络（ISEANet），通过稀疏子段引导降噪层和轻量多特征提取模块增强子域表示，显著提升了滚动轴承无监督跨域故障诊断的准确性和可解释性。
- Jianhua Zhong;Cong Lin;Yang Gao;Jianfeng Zhong;Shuncong Zhong等人{Fault diagnosis of rolling bearings under variable conditions based on unsupervised domain adaptation method}针对变工况下滚动轴承故障诊断中目标域数据缺失标签且与源域数据分布差异大的问题，提出基于无监督深度卷积动态联合分布域自适应网络模型，通过动态对齐两域特征的边缘分布和条件分布，实现了仅依赖源域标签即可准确分类目标域样本的突破。
- Cuixiang Wang ;Shengkai Wu ;Xing Shao等人{Unsupervised domain adaptive bearing fault diagnosis based on maximum domain discrepancy}针对现有基于域适应的轴承故障诊断方法中源域与目标域特征差异不明显、特征提取器参数趋同导致诊断性能不佳的问题，提出基于最大域差异的无监督域自适应方法，通过最大化域间特征差异同时欺骗判别器，显著提升了跨域故障诊断的准确性和鲁棒性。
- Zheng Bo;Huang Jianhao;Ma Xin;Zhang Xiaoqiang;Zhang Qiang等人{An unsupervised transfer learning method based on SOCNN and FBNN and its application on bearing fault diagnosis}针对嘈杂环境中轴承相似故障诊断能力不足及对标记数据依赖性强的问题，提出基于结构优化卷积神经网络和快速批量核范数最大化的无监督迁移学习方法，通过优化特征提取与域间分布对齐显著提升了诊断精度。
- Fan Xu;Duo Hong;Yawen Tian;Naizhen Wei;Jianwei Wu等人{Unsupervised Deep Transfer Learning Method for Rolling Bearing Fault Diagnosis Based on Improved Convolutional Neural Network}针对滚动轴承在无监督域差异场景下故障诊断的难题，提出结合卷积核随机失活、跳跃连接和联合最大均值差异的JMMD-CKDSCNet方法，显著提升了模型在目标域无标签数据条件下的泛化性能。
- Fu Haiyue;Yu Di;Zhan Changshu;Zhu Xiangzhen;Xie Zhijie等人{Unsupervised rolling bearing fault diagnosis method across working conditions based on multiscale convolutional neural network}针对滚动轴承在不同工况下振动信号分布变化且目标工况样本标签难以获取的问题，提出基于多尺度特征提取与改进1D-ConvNeXt架构的深度子域自适应卷积神经网络方法，通过融合高低层特征并引入通道注意力机制，实现了无监督跨工况故障诊断的显著性能提升。
- Huo Tianlong;Deng Linfeng;Zhang Bo;Gong Jun;Hu Baoquan;Zhao Rongzhen;Liu Zheng等人{Novel imbalanced subdomain adaption multiscale convolutional network for cross-domain unsupervised fault diagnosis of rolling bearings}针对滚动轴承故障诊断中数据分布不平衡且跨域工况下无标签数据难以利用的问题，提出一种结合多尺度特征提取、注意力机制和新型损失函数的子域自适应网络，实现了对不平衡数据的准确分类和跨域特征的有效对齐。
- Tang Guiting;Yi Cai;Liu Lei;Xing Zhan;Zhou Qiuyang;Lin Jianhui等人{Integrating adaptive input length selection strategy and unsupervised transfer learning for bearing fault diagnosis under noisy conditions}针对噪声条件下轴承故障诊断中迁移学习性能下降的问题，提出一种结合自适应输入长度选择、宽核卷积去噪和分布对齐优化的无监督迁移学习方法，显著提升了模型在工程噪声环境中的诊断准确性和泛化能力。
- Huo Chunran;Jiang Quansheng;Shen Yehu;Lin Xiaoshan;Zhu Qixin;Zhang Qingkui等人{A class-level matching unsupervised transfer learning network for rolling bearing fault diagnosis under various working conditions}针对滚动轴承在不同工况下无监督故障诊断时域级特征匹配忽略类别分布的问题，提出基于最大分类器差异结构的类级匹配迁移学习网络，通过结合域级匹配、类级匹配和目标域伪标签直接指导的三阶段训练方法，实现了更精准的故障特征提取。
- Zhidan Zhong;Hao Liu;Wentao Mao;Xinghui Xie;Yunhao Cui等人{Rolling Bearing Fault Diagnosis across Operating Conditions Based on Unsupervised Domain Adaptation}针对滚动轴承在不同工况下源域与目标域数据分布不一致且目标域无标签的诊断难题，提出基于卷积自编码器深度特征构建与平衡分布自适应的方法，实现了跨工况的无监督域适应故障诊断。
- Chen Pengfei;Zhao Rongzhen;He Tianjing;Wei Kongyuan;Yuan Jianhui等人{Unsupervised structure subdomain adaptation based the Contrastive Cluster Center for bearing fault diagnosis}针对轴承故障诊断中传统无监督域适应方法忽略子域分布差异和伪标签噪声的问题，提出基于对比聚类中心的子域对齐方法，通过过滤噪声伪标签和拉近同类子域中心来提升诊断精度。
- Tao Hongfeng;Qiu Jier;Chen Yiyang;Stojanovic Vladimir;Cheng Long等人{Unsupervised cross-domain rolling bearing fault diagnosis based on time-frequency information fusion}针对滚动轴承故障诊断中标签数据难以获取且样本分布差异大的问题，提出基于时频信息融合的无监督跨域诊断方法，通过改进的最大均值差异算法计算联合分布距离，实现了无需标签的跨工况故障诊断。
- Nguyen Duc Thuan;Nguyen Thi Hue;Hoang Si Hong等人{Unsupervised Bearing Fault Diagnosis via a Multi-Layer Subdomain Adaptation Network}针对工业场景中轴承故障诊断数据标注困难的问题，提出一种基于多层子域适配的无监督迁移学习方法，通过减小可获取数据与未标注实际数据间的分布差异，显著提升了跨机器故障诊断的准确性和实用性。
- 黄友锐;戴宇等人{基于多尺度图卷积神经网络的域自适应轴承故障诊断方法}针对轴承故障诊断中域自适应方法难以提取细微特征且单一度量函数无法全面刻画域间复杂关系的问题，提出基于多尺度图卷积神经网络的方法，通过三级特征提取架构和加权联合差异对齐函数实现局部与全局域校准，显著提升了跨工况诊断的精度与鲁棒性。
- 王萌璠;蔡宗琰;田心平;周昌等人{基于LMMD-DANN的无监督风电轴承故障诊断方法}针对变工况下风电轴承故障诊断因目标域数据无标签导致性能下降的问题，提出基于LMMD-DANN的无监督诊断方法，通过域对抗机制和局部特征对齐增强特征提取能力，实现了跨域数据的高精度诊断，在多个数据集上验证了其优越性。

综合来看，“统计分布对齐方法（MMD/LMMD/子域对齐）”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2023–2025 年。代表性的研究包括 黄友锐;戴宇、Shouqiang Kang;Yulin Sun;Xinrui Li;Yujing Wang;Qingyan Wang;Xintao Liang、崔朝阳;杨绍普;顾晓辉;申永军 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 对抗式迁移与表示不变性学习

“对抗式迁移与表示不变性学习”这一小类主要汇总了 21 篇相关工作，时间范围大致覆盖 2023–2026 年。

- Chaoge Wang;Xinyu Tian;Funa Zhou;Hamid Reza Karimi等人{Intelligent fault diagnosis of bearings based on unsupervised domain adaptive adversarial graph neural network under variable operating conditions}针对工业设备故障诊断中标签稀缺和时变数据分布的双重挑战，提出基于无监督域自适应对抗图神经网络的方法，通过融合类别标签、域标签和数据结构信息，显著提升了变工况下轴承故障诊断的准确性和适应性。
- Chen Liu;Runshan Hu;Xuan Fang;Weibin Luo;Chenyang Zhu等人{Enhancing unsupervised bearing fault diagnosis through structured prediction in latent subspace}针对工业设备故障诊断中标签稀缺和类别不平衡问题，提出一种基于潜在子空间结构化预测的无监督域适应框架，通过条件域对抗网络合成故障信号并提取域不变特征，显著提升了模型在真实场景中的泛化能力。
- Zhihui Men;Dao Gong;Kai Zhou;Yuejian Chen;Jinsong Zhou等人{Unsupervised domain adaptation method for bearing fault diagnosis assisted by twin data under extreme sample scarcity}针对小样本轴承故障诊断中合成信号因缺乏真实噪声和非线性特征导致与真实数据存在域差异的问题，提出一种基于风格迁移的端到端方法生成更逼真的孪生数据，并通过无监督域适应提升诊断性能，显著缓解了极端样本稀缺条件下的诊断难题。
- Lin Song;Yanlin Zhao;Junjie He;Simin Wang;Boyang Zhong;Fei Wang等人{MAJATNet: A Lightweight Multi-Scale Attention Joint Adaptive Adversarial Transfer Network for Bearing Unsupervised Cross-Domain Fault Diagnosis}针对滚动轴承在不同工况下振动数据差异导致故障诊断不准确的问题，提出基于轻量级多尺度注意力联合自适应对抗迁移网络MAJATNet的方法，其最突出的贡献是通过一维多尺度注意力残差结构和改进的IJA损失函数有效缩小跨域特征分布差异，显著提升了无监督跨域故障诊断的准确性。
- Lei Liu;Weihua Zhang;Fengshou Gu;Dongli Song;Guiting Tang;Yao Cheng等人{An unsupervised transfer network with adaptive input and dynamic channel pruning for train axle bearing fault diagnosis}针对列车车轴轴承故障诊断中现有方法输入长度固定且对噪声敏感的跨域诊断问题，提出一种具有自适应输入和动态通道剪枝的无监督迁移网络，通过自适应选择输入长度和增强特征学习，显著提升了在噪声污染目标域中的诊断鲁棒性和准确性。
- 林亚团;王子逢;彭晶等人{分类性差异对抗自适应的无监督轴承故障诊断}针对工业轴承故障诊断中跨域数据分布差异显著、标注数据稀缺及传统域自适应方法忽视子域边界信息的问题，提出一种基于分类性差异对抗自适应网络的无监督诊断方法，通过子域边界精细化对齐、对抗自适应特征生成与多模态故障分类框架，显著提升了跨域特征一致性和复杂故障模式的分类精度，为工业轴承智能运维提供了高精度、强鲁棒性的解决方案。
- 汪振鹏等人{基于半监督与无监督迁移学习的滚动轴承故障诊断研究}针对滚动轴承故障诊断中工况复杂多变、故障样本稀缺导致传统方法泛化能力不足的问题，提出结合半监督与无监督迁移学习的方法，通过决策边界自适应和交叉注意力机制提升模型在变工况下的诊断准确性和鲁棒性，显著增强了故障诊断的实用性和适应性。
- 贡莹莹等人{基于深度迁移学习的轴承故障诊断研究}针对轴承故障诊断中工况多变导致模型泛化性差、未知故障识别困难的问题，提出基于深度迁移学习的多尺度子领域自适应和多源开放集领域自适应方法，有效提升了模型在闭集和开放集设定下的泛化性能与未知故障识别能力。
- 渠笑添等人{基于卷积神经网络的变转速工况轴承故障诊断方法研究}针对变转速工况下轴承故障特征提取困难、目标域数据稀缺导致模型泛化能力不足的问题，提出基于卷积神经网络的多任务诊断模型与双框架孪生网络迁移算法，开发了智能诊断软件，有效提升了复杂工况下的故障诊断可靠性与智能化水平。
- 耿源浩等人{基于联合分布对齐对抗迁移的轴承故障诊断方法研究}针对轴承故障诊断中源域标签不足、目标域存在未知故障类型及未知工况缺乏先验数据分布等问题，提出基于联合分布对齐对抗迁移的方法，通过结合对抗学习与分布对齐机制，在跨工况、开集和未知工况场景下实现了更精准的故障分类，显著提升了诊断模型的泛化能力和实用性。
- Kaitong Jia;Xin Wen;Gang Chen等人{Interpretable Knowledge Transfer with a Novel Structure Discrepancy Metrics for Unsupervised Bearing Fault Diagnosis from Simulation to Reality}针对无监督轴承故障诊断中仿真数据与真实数据间的知识迁移难题，提出基于小波时序逻辑网络和时序逻辑差异度量的可解释迁移学习框架，通过增强损失函数定义实现高精度诊断并提升模型可解释性。
- 杨军等人{基于深度迁移学习的轴承故障诊断方法研究}针对轴承故障诊断中跨工况/跨设备数据分布差异大、标注困难、传统方法泛化能力不足的问题，提出改进领域对抗网络和领域分离网络的三种新型深度迁移学习方法，显著提升了跨工况和跨设备诊断的准确率与稳定性。
- Ning Jia;Weiguo Huang;Chuancang Ding;Jun Wang;Zhongkui Zhu等人{Physics-informed unsupervised domain adaptation framework for cross-machine bearing fault diagnosis}针对工业设备监测数据分布差异大且标注困难的问题，提出融合物理信息与数据驱动的无监督域适应框架，通过物理损失函数增强模型可靠性与可解释性，显著提升了跨机器轴承故障诊断的泛化能力。
- Chunran Huo;Weiyang Xu;Quansheng Jiang;Yehu Shen;Qixin Zhu;Qingkui Zhang等人{An unsupervised transfer learning approach for rolling bearing fault diagnosis based on dual pseudo-label screening}针对滚动轴承故障诊断中伪标签质量依赖网络自身易导致样本误分类的问题，提出基于预测标签变化信息的双重样本筛选方法，通过结合预筛选与实时筛选消除训练过程中的预测误差样本，显著提升了无监督迁移学习在变工况条件下的诊断稳定性。
- Wang Haomiao;Li Yibin;Jiang Mingshun;Zhang Faye等人{Multiscale convolutional conditional domain adversarial network with channel attention for unsupervised bearing fault diagnosis}针对轴承故障诊断中多尺度特征重要性不一致、冗余信息多以及跨域诊断忽略类别信息导致多模态结构捕获失败的问题，提出一种结合通道注意力机制和多尺度卷积的条件域对抗网络方法，通过突出有价值特征并充分捕捉多模态结构，显著提升了无监督跨域故障诊断的准确性。
- Pang Bin;Liu Qiuhai;Sun Zhenduo;Xu Zhenli;Hao Ziyang等人{Time-frequency supervised contrastive learning via pseudo-labeling: An unsupervised domain adaptation network for rolling bearing fault diagnosis under time-varying speeds}针对滚动轴承在变转速工况下数据分布偏移导致故障诊断模型泛化能力差的问题，提出基于伪标签的时频监督对比学习方法，通过提取速度不变的类不变特征，有效提升了无监督跨转速故障诊断的准确性。
- Wang Gongxian;Zhang Teng;Hu Zhihui;Zhang Miao等人{A Novel Lightweight Unsupervised Multi-branch Domain Adaptation Network for Bearing Fault Diagnosis Under Cross-Domain Conditions}针对轴承故障诊断中跨域条件下单通道提取域不变特征质量不足的问题，提出一种结合多尺度平均处理和多分支结构的轻量级无监督域适应网络，通过对抗学习和分布对齐策略显著提升了跨域诊断性能。
- Li Xueyi;Yuan Peng;Wang Xiangkai;Li Daiyou;Xie Zhijie;Kong Xiangwei等人{An unsupervised transfer learning bearing fault diagnosis method based on depthwise separable convolution}针对轴承故障诊断中标记数据稀缺且传统方法依赖大量标注的问题，提出基于深度可分离卷积的改进自适应批量归一化迁移学习方法，通过冻结网络参数并仅调整批量归一化层，实现了在少量标记数据下的高精度故障诊断。
- Yao Li;Rui Yang;Hongshu Wang等人{Unsupervised Method Based on Adversarial Domain Adaptation for Bearing Fault Diagnosis}针对轴承故障诊断中深度学习网络过拟合、计算效率低和梯度消失等问题，提出基于对抗域适应的无监督方法，通过改进瓶颈残差块特征提取器结合DANN和MCD模型，实现了最高100%的分类准确率，显著提升了跨域故障诊断性能。
- Ma Wengang;Zhang Yadong;Ma Liang;Liu Ruiqi;Yan Shan等人{An unsupervised domain adaptation approach with enhanced transferability and discriminability for bearing fault diagnosis under few-shot samples}针对动车组轴承在特殊工况下缺乏足够标记数据（少样本）导致故障诊断困难的问题，提出一种增强可迁移性与可判别性的无监督域自适应方法（ETDS-UDA），通过构建高效特征提取器与优化策略，显著提升了少样本条件下的故障诊断精度与模型泛化能力。
- 谢秀煌;俞炅旻;符栋梁;高伟等人{基于多域特征融合和迁移学习的跨机器轴承故障诊断方法}针对跨机器轴承故障诊断中异构数据分布导致的领域偏移问题，提出一种结合多域特征融合与迁移学习的网络方法，通过冻结主干网络参数与低秩自适应优化策略，并融合希尔伯特变换和格拉姆角场的多模态特征，显著提升了模型泛化能力与计算效率，在跨域诊断任务中实现最高98.5%的准确率且参数量减少90%以上。

综合来看，“对抗式迁移与表示不变性学习”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2023–2026 年。代表性的研究包括 谢秀煌;俞炅旻;符栋梁;高伟、Chaoge Wang;Xinyu Tian;Funa Zhou;Hamid Reza Karimi、Chen Liu;Runshan Hu;Xuan Fang;Weibin Luo;Chenyang Zhu 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 多源域泛化与未知工况鲁棒性

“多源域泛化与未知工况鲁棒性”这一小类主要汇总了 8 篇相关工作，时间范围集中在 2025 年左右。

- 康津;马萍;张宏立;王聪;李新凯等人{基于联邦域泛化的未知工况下滚动轴承故障诊断框架}针对联邦学习在未知工况下故障诊断模型泛化性能下降且需保护数据隐私的问题，提出融合元学习与知识蒸馏的联邦域泛化框架，通过增强模型领域不变性和任务适应能力，显著提升了模型在未知工况下的诊断准确性与适应性。
- 李庆;周公博;周坪;闫晓东;韩链锋;李强;马国庆等人{基于多维信息协同神经网络的轴承跨工况故障诊断}针对轴承复杂工况下监测数据采集困难导致的不完备信息跨工况故障诊断问题，提出基于多维信息协同神经网络的方法，通过协同归一化策略和多维时空特征融合模块减少协变量偏移并增强域不变特征提取，在多个数据集上实现了优于主流方法的诊断准确率。
- 朱继扬;李邦;蔡海;丁晓明等人{基于1D TRLTN的未知工况滚动轴承故障诊断}针对碟式分离机因工况多变导致滚动轴承故障数据获取困难且无法预知未知工况样本的问题，提出基于一维三叉戟表示学习迁移网络（1D TRLTN）的方法，通过多卷积结构提取特征、知识蒸馏与动态分布适应融合不变特征，实现了未知工况下的高精度故障诊断，显著提升了诊断准确率并为设备安全运行提供技术保障。
- 向佳伟等人{面向滚动轴承的域泛化故障诊断方法研究与系统开发}针对滚动轴承故障诊断中数据分布差异导致的模型泛化能力不足问题，提出一种域泛化方法，通过开发相应系统实现了跨工况下的稳定诊断，显著提升了诊断模型的适应性和实用性。
- Guoli Bai;Tonghao Xing;Wei Sun;Huashan Chi;Zhidan Zhong;Qingchao Sun;Liang Sun等人{Unsupervised multiple-target domain adaptation for bearing fault diagnosis}针对轴承故障诊断中多工况下数据分布差异和标签缺失导致模型泛化能力受限的问题，提出一种无监督多目标域自适应方法，通过同时确保特征的域不变性和故障相关性，实现了跨多个未标记工况的准确故障诊断。
- 黄嘉龙等人{基于领域泛化的轴承故障诊断方法研究}针对轴承故障诊断中单源域数据稀缺、跨工况分布差异大及多源域过拟合特定源域的问题，提出融合多模态特征与对抗生成网络的跨域数据增强、多损失协同优化和自适应多源集成方法，显著提升了跨域泛化性能，最高准确率达95.1%。
- 杨国军等人{基于数据增强和不变特征提取的故障诊断域泛化方法研究}针对滚动轴承故障诊断中数据不平衡、无关特征干扰和单一模态局限的域泛化问题，提出基于数据增强、不变特征提取和多模态融合的创新方法，显著提升了模型在不同工况下的跨域诊断精度和泛化能力。
- 乔卉卉;赵二贤;郝如江;刘婕;刘帅;王勇超等人{基于多尺度CNN与双阶段注意力机制的轴承工况域泛化故障诊断}针对变工况条件下轴承故障诊断因领域漂移导致模型准确率降低且难以获取目标工况样本的问题，提出基于多尺度CNN与双阶段注意力机制的TSAMCNN模型，通过提取工况域不变故障特征，显著提升了诊断准确率、抗噪性能和工况域泛化能力，并增强了模型可解释性。

综合来看，“多源域泛化与未知工况鲁棒性”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 康津;马萍;张宏立;王聪;李新凯、李庆;周公博;周坪;闫晓东;韩链锋;李强;马国庆、朱继扬;李邦;蔡海;丁晓明 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


## 数据受限场景下的智能诊断


### 小样本与度量学习方法

“小样本与度量学习方法”这一小类主要汇总了 3 篇相关工作，时间范围集中在 2025 年左右。

- 王子卓等人{基于增强卷积神经网络的小样本滚动轴承故障诊断方法研究}针对滚动轴承故障诊断中特征提取难、小样本及跨工况泛化弱等问题，提出基于增强卷积神经网络（如ConvNeXt改进架构）结合时频图像化表征与优化算法的协同诊断方法，显著提升了小样本下的诊断准确率与跨工况泛化能力，为工业设备智能运维提供了新路径。
- 陶旭等人{基于度量学习的小样本轴承故障诊断研究}针对轴承故障样本收集困难导致深度学习模型诊断准确率低的问题，提出基于度量学习的E-ND4、CMBDC和AMFSFD方法，通过改进特征提取、引入注意力机制和对抗学习，显著提升了小样本条件下的故障诊断准确率和泛化能力。
- 刘帅等人{不完备数据条件下基于深度学习的列车轮对轴承故障诊断方法研究}针对货运列车轮对轴承故障样本难以获取、标签缺失和工况时变导致深度学习诊断精度不足的问题，提出基于数据增强、域适应和域泛化技术的方法，显著提升了小样本、跨工况和未知工况条件下的故障诊断准确率。

综合来看，“小样本与度量学习方法”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 王子卓、陶旭、刘帅 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 自监督/对比学习与特征增强

“自监督/对比学习与特征增强”这一小类主要汇总了 3 篇相关工作，时间范围大致覆盖 2024–2025 年。

- Shijing Cao;Yuxin Duan;Jin Huang等人{An interpretable unsupervised fault diagnosis method for rolling bearings based on physically-informed pseudo-label updating}针对工业设备运行中产生大量无标签数据导致传统数据驱动模型性能下降且缺乏物理可解释性的问题，提出基于物理信息伪标签动态更新的无监督神经网络方法，通过结合数据驱动学习与物理约束并引入正则化机制，显著提升了滚动轴承故障诊断的泛化能力和可解释性。
- Pengping Luo;Zhiwei Liu等人{Unsupervised Bearing Fault Diagnosis Using Masked Self-Supervised Learning and Swin Transformer}针对轴承故障诊断依赖人工特征和标注数据的问题，提出结合掩码自监督学习和Swin Transformer的无监督框架，通过重构预训练从无标签振动信号中学习鲁棒特征，显著提升对未知故障的检测精度，在多个数据集上达到99.53%至100%的准确率。
- Lei Wang;Hang Rao;Zhengcheng Dong;Wenhui Zeng;Fan Xu;Li Jiang;Chao Zhou等人{Automatic fault diagnosis of rolling bearings under multiple working conditions based on unsupervised stack denoising autoencoder}针对滚动轴承在无标签数据条件下难以进行故障诊断的问题，提出基于无输出层堆叠去噪自编码器的无监督自动诊断方法，通过特征提取和降维减少对人工标注的依赖，实现了多工况下的自动故障识别。

综合来看，“自监督/对比学习与特征增强”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2024–2025 年。代表性的研究包括 Shijing Cao;Yuxin Duan;Jin Huang、Pengping Luo;Zhiwei Liu、Lei Wang;Hang Rao;Zhengcheng Dong;Wenhui Zeng;Fan Xu;Li Jiang;Chao Zhou 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


### 标签稀缺条件下的增量与持续学习

“标签稀缺条件下的增量与持续学习”这一小类主要汇总了 1 篇相关工作，时间范围集中在 2025 年左右。

- 王磊等人{基于注意力机制与增量学习的水泵机组轴承故障诊断方法研究}针对水泵机组滑动轴承振动信号受噪声干扰且传统方法难以捕捉瞬态特征、无法处理未知故障的问题，提出结合注意力机制与增量学习的方法，通过多分支特征融合和知识蒸馏技术，显著提升了故障诊断精度并有效抑制了模型对新故障的遗忘。

综合来看，“标签稀缺条件下的增量与持续学习”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 王磊 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。


## 工程化诊断系统与可部署方法


### 数字孪生与机理-数据融合建模

“数字孪生与机理-数据融合建模”这一小类主要汇总了 2 篇相关工作，时间范围集中在 2025 年左右。

- Zhenli Xu;Guiji Tang;Bin Pang等人{Simulation-driven unsupervised fault diagnosis of rolling bearing under time-varying speeds}针对变转速条件下滚动轴承故障样本稀缺且故障特征时变导致深度学习诊断困难的问题，提出基于分析式故障仿真模型生成匹配变转速条件的高质量数据，并设计多尺度增强时序卷积Transformer网络提取鲁棒特征的无监督诊断方法，实现了变转速工况下无需真实故障标签的准确故障诊断。
- 花兴等人{基于机理—数据融合的噪声条件下滚动轴承故障诊断方法研究}针对强噪声干扰和小样本数据条件下滚动轴承故障难以有效识别的问题，提出基于机理-数据融合的噪声条件下滚动轴承故障诊断方法，通过构建动力学模型生成仿真信号、结合SPAVMD与WOA-LSSVM的鲁棒智能诊断方法以及融合机理与数据的迁移学习框架，显著提升了噪声环境下的故障诊断精度和泛化性能。

综合来看，“数字孪生与机理-数据融合建模”这一小类的工作主要围绕若干关键问题展开，相关研究大致分布在 2025 年。代表性的研究包括 Zhenli Xu;Guiji Tang;Bin Pang、花兴 等人的工作，这些方法在公开数据集上验证了有效性，为后续在真实工程场景中的推广应用奠定了基础，但在跨工况泛化能力、可解释性以及与实际工业流程的深度融合方面仍有进一步提升空间。
