Phần I. MỞ ĐẦU
Giới thiệu đề tài
Quản lý rác thải hiệu quả là một thách thức toàn cầu cấp thiết. Việc phân loại rác thải thủ công thường kém hiệu quả, nguy hại và tốn kém. Dự án này trình bày chi tiết về việc phát triển "Hệ thống Nhận dạng và Phân loại Rác thải", một ứng dụng được thiết kế để tự động hóa quy trình phân loại rác thải bằng công nghệ thị giác máy tính và học sâu.
Mục tiêu cốt lõi của hệ thống là phân loại chính xác các loại rác thải từ hình ảnh thành các loại riêng biệt: bìa cứng, rác thải điện tử, thủy tinh, y tế, kim loại, giấy và nhựa.
Bằng cách tận dụng Mạng Nơ-ron Tích chập (CNN) mạnh mẽ, hệ thống này cung cấp một giải pháp có khả năng mở rộng và hiệu quả để hợp lý hóa quy trình tái chế, giảm thiểu ô nhiễm trong các luồng tái chế và thúc đẩy môi trường trong sạch hơn. Các công nghệ chính được sử dụng trong dự án này là TensorFlow/Keras để huấn luyện mô hình, OpenCV để xử lý hình ảnh, Flask để tạo API web và SQL Server để lưu trữ dữ liệu.
Mục tiêu nghiên cứu
Xây dựng một mô hình CNN có khả năng nhận dạng và phân loại chính xác các loại rác thải dựa trên hình ảnh.
Tích hợp mô hình AI vào một ứng dụng web động cho phép người dùng tải ảnh hoặc sử dụng camera để nhận diện rác theo thời gian thực.
Xử lý thời gian thực (Real-time) bằng cách ứng dụng công nghệ xử lý ảnh (OpenCV) để phân loại rác trực tiếp thông qua Camera/Webcam.
Xây dựng chức năng quản trị (Admin) để cung cấp công cụ cho quản trị viên để quản lý người dùng, quản lý danh mục rác và xem các báo cáo thống kê về hoạt động của hệ thống.
Thiết kế cơ sở dữ liệu SQL Server để lưu trữ thông tin người dùng, lịch sử phân loại và phản hồi, phục vụ cho việc thống kê và huấn luyện lại mô hình sau này.
Phạm vi và giới hạn đề tài
Phạm vi:
Hệ thống hoạt động trên hình ảnh rác thải thu thập từ nguồn dữ liệu công khai (như TrashNet, Kaggle, hoặc ảnh tự thu thập).
Hệ thống xử lý ảnh tĩnh hoặc luồng video đơn giản trong thời gian thực thông qua webcam.
Đối tượng sử dụng: Người dùng phổ thông (phân loại rác) và Quản trị viên (quản lý hệ thống).
Giới hạn:
Mô hình CNN được huấn luyện trên tập dữ liệu có giới hạn, do đó có thể gặp sai số khi gặp rác ở điều kiện ánh sáng hoặc góc nhìn khác biệt.
Hệ thống hiện tại chưa tích hợp phần cứng IoT hoặc robot phân loại vật lý.
Việc xử lý được thực hiện trên máy chủ cục bộ (Localhost), chưa triển khai trên nền tảng đám mây (Cloud).
Phân loại giới hạn trong 7 loại rác cụ thể, chưa bao quát toàn bộ các loại rác trong thực tế.
Kiến trúc hệ thống
Hệ thống hoạt động theo quy trình tuần tự, từ chụp ảnh đến lưu trữ phân loại cuối cùng.
Thu nhận hình ảnh (Image Capture): Hệ thống nhận ảnh đầu vào từ webcam hoặc ảnh được tải lên bởi người dùng.
Tiền xử lý hình ảnh: Hình ảnh đầu vào được ứng dụng tiền xử lý. Quá trình này bao gồm việc thay đổi kích thước hình ảnh theo kích thước yêu cầu (224x224 pixel) và chuẩn hóa các giá trị pixel trong phạm vi [0, 1] để phù hợp với mô hình CNN.
API Dự đoán (Flask): Hình ảnh đã được tiền xử lý được gửi qua yêu cầu HTTP đến điểm cuối API Flask.
Mô hình AI (TensorFlow/Keras): Ứng dụng Flask tải mô hình CNN đã được đào tạo trước (best_model.h5). Mô hình xử lý hình ảnh và đưa ra dự đoán, cho biết xác suất cho từng loại chất thải.
Kết quả Phân loại: API xác định loại có xác suất cao nhất là dự đoán cuối cùng và gửi kết quả này trở lại trong phản hồi API.
Lưu trữ cơ sở dữ liệu (SQL Server): Kết quả phân loại, cùng với dấu thời gian và đường dẫn tệp hình ảnh (tùy chọn), được ghi vào cơ sở dữ liệu SQL Server để theo dõi và phân tích.
Phương pháp nghiên cứu
Phương pháp thu thập dữ liệu:
Dữ liệu được lấy từ bộ dữ liệu công khai (TrashNet, Waste Classification Dataset, v.v.) hoặc thu thập thủ công từ Internet và môi trường thực tế.
Mỗi ảnh được gắn nhãn thủ công theo 7 loại rác thải: bìa cứng, điện tử, thủy tinh, y tế, kim loại, giấy và nhựa.
Phương pháp xử lý dữ liệu:
Tiền xử lý ảnh gồm thay đổi kích thước, chuẩn hóa pixel, và data augmentation (xoay, lật, thay đổi độ sáng) để tăng tính đa dạng cho tập dữ liệu huấn luyện.
Phương pháp xây dựng mô hình:
Thiết kế và huấn luyện mô hình CNN bằng TensorFlow/Keras với các lớp convolution, pooling và fully connected. Sử dụng categorical_crossentropy làm hàm mất mát và Adam optimizer để tối ưu.
Chia tập dữ liệu thành 80% huấn luyện và 20% kiểm thử.
Phương pháp đánh giá mô hình:
Sử dụng các chỉ số Accuracy, Precision, Recall, và F1-Score để đo lường hiệu quả. Quan sát biểu đồ loss/accuracy và ma trận nhầm lẫn để đánh giá khả năng phân loại từng loại rác.
Phương pháp triển khai ứng dụng:
Xây dựng Flask API kết nối mô hình CNN và cơ sở dữ liệu SQL Server.
Tạo giao diện web đơn giản bằng HTML/CSS/JS cho phép người dùng tương tác với hệ thống.
Sử dụng OpenCV để bắt hình ảnh từ camera hoặc upload hình ảnh và gửi về server xử lý.
Kiểm thử hệ thống trên máy chủ cục bộ, đảm bảo khả năng phản hồi nhanh và chính xác. 
Phần II. CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ
Tổng quan về Trí tuệ nhân tạo (AI)

Hình 1: Artificial Intelligence – AI (Trí tuệ nhân tạo)
Trí tuệ nhân tạo là lĩnh vực nghiên cứu nhằm tạo ra các hệ thống máy tính có khả năng mô phỏng tư duy và hành vi của con người, như học tập, lập luận, ra quyết định và xử lý ngôn ngữ tự nhiên.
AI ngày nay được ứng dụng rộng rãi trong nhiều lĩnh vực như: nhận dạng hình ảnh, xe tự hành, robot, y tế, tài chính và đặc biệt là xử lý thị giác máy tính.
AI có thể được chia thành ba cấp độ:
AI hẹp (Narrow AI): thực hiện một nhiệm vụ cụ thể, ví dụ như nhận dạng khuôn mặt hoặc giọng nói.
AI tổng quát (General AI): có khả năng hiểu, học và áp dụng tri thức như con người (chưa đạt được trong thực tế).
AI siêu việt (Super AI): vượt trội hơn con người về mọi mặt tư duy (chỉ tồn tại trong lý thuyết).
Tổng quan về Thị giác máy tính (Computer Vision)

Hình 2: Computer Vision (Thị giác máy tính)
Thị giác máy tính là một nhánh của AI giúp máy tính hiểu và diễn giải hình ảnh hoặc video từ thế giới thực.
Nói cách khác, Computer Vision cho phép máy tính “nhìn thấy” và “hiểu” được nội dung trong hình ảnh tương tự như con người.
Quy trình xử lý trong thị giác máy tính thường gồm các bước:
Thu nhận hình ảnh: từ camera, cảm biến hoặc dữ liệu có sẵn.
Tiền xử lý: điều chỉnh kích thước, lọc nhiễu, cân bằng sáng, chuẩn hóa dữ liệu.
Trích xuất đặc trưng (Feature Extraction): xác định các đặc điểm quan trọng như cạnh, hình dạng, màu sắc.
Nhận dạng và phân loại: sử dụng các thuật toán học máy hoặc mạng nơ-ron để xác định đối tượng trong ảnh.
Ứng dụng của Computer Vision:
Nhận dạng khuôn mặt và vật thể.
Giám sát an ninh bằng camera.
Phân loại rác thải, sản phẩm trong công nghiệp.
Hệ thống xe tự lái.
Phân tích ảnh y khoa.
Tổng quan về Deep Learning (học sâu)
Học sâu (deep learning) là một tập hợp con của học máy (machine learning), tập trung vào việc xây dựng và huấn luyện mạng nơ-ron nhiều lớp, được gọi là mạng nơ-ron sâu (DNN – Deep neural networks) để chúng có thể tự động học, hiểu dữ liệu, mô phỏng khả năng ra quyết định phức tạp của bộ não con người.
Mô hình học sâu có thể nhận diện nhiều hình mẫu phức tạp trong hình ảnh, văn bản, âm thanh và các dữ liệu khác để tạo ra thông tin chuyên sâu và dự đoán chính xác. Bạn có thể sử dụng các phương pháp học sâu để tự động hóa các tác vụ thường đòi hỏi trí tuệ con người, chẳng hạn như phân loại hình ảnh hoặc chép lời một tập tin âm thanh.
Các ứng dụng của Deep Learning: Chatbot, nhận diện khuôn mặt, khoa học y tế, nhận dạng giọng nói,...
Cách hoạt động:
Mạng nơ-ron sâu (Deep neural network) hoặc mạng nơ-ron nhân tạo (Artificial neural network) cố gắng bắt chước bộ não con người thông qua sự kết hợp của dữ liệu đầu vào, trọng số và độ lệch. Các phần tử này phối hợp với nhau để nhận dạng, phân loại và mô tả chính xác các đối tượng trong dữ liệu.
Mạng nơ-ron sâu (Deep neural network) bao gồm nhiều lớp node được kết nối với nhau, mỗi lớp được xây dựng dựa trên lớp trước đó để tinh chỉnh và tối ưu hóa dự đoán hoặc phân loại. Tiến trình tính toán này thông qua mạng được gọi là truyền xuôi (forward propagation).
Các lớp đầu vào và đầu ra của mạng nơ-ron sâu (Deep neural network) được gọi là các lớp hiển thị. Lớp đầu vào là nơi mô hình deep learning nhập dữ liệu để xử lý và lớp đầu ra là nơi đưa ra dự đoán hoặc phân loại cuối cùng.
Một quy trình khác gọi là truyền ngược (back propagation) sử dụng các thuật toán như giảm độ dốc, để tính toán các lỗi trong dự đoán, sau đó điều chỉnh trọng số và độ lệch của hàm bằng cách di chuyển ngược qua các lớp trong mô hình.
Truyền ngược và truyền xuôi cho phép mạng nơ-ron sâu đưa ra dự đoán và sửa lỗi ngay lập tức. Theo thời gian, thuật toán dần trở nên chính xác hơn.

Hình 3: Deep Learning (học sâu)
Các loại mô hình học sâu
Mạng nơ-ron tích chập (CNN – Convolutional Neural Network): CNN được sử dụng để nhận dạng và xử lý hình ảnh. Chúng đặc biệt giỏi trong việc xác định các đối tượng trong ảnh, ngay cả khi các đối tượng đó bị che khuất hoặc biến dạng một phần.
Học tăng cường (RL – Reinforcement Learning): Học tăng cường sâu được sử dụng cho chế tạo robot và chơi trò chơi. Đó là một loại máy học cho phép một tác nhân học cách cư xử trong môi trường bằng cách tương tác với môi trường đó và nhận phần thưởng hoặc hình phạt.
Mạng nơ-ron hồi quy (RNNs – Recurrent Neural Networks): RNN được sử dụng để xử lý ngôn ngữ tự nhiên và nhận dạng giọng nói. Chúng đặc biệt giỏi trong việc hiểu ngữ cảnh của câu hoặc cụm từ, được sử dụng để tạo văn bản hoặc dịch ngôn ngữ.
Mạng nơ-ron biến áp (TNN – Transformer Neural Network): Transformer sử dụng cơ chế chú ý (attention mechanism) để học được mối quan hệ giữa các phần tử trong dữ liệu đầu vào, giúp mô hình đạt được hiệu quả cao hơn so với RNN trong nhiều nhiệm vụ. Ví dụ: tóm tắt văn bản, trả lời câu hỏi, xử lý ngôn ngữ tự nhiên,…
Mạng đối nghịch tạo sinh (GAN – Generative Adversarial Networks): GAN bao gồm hai mạng nơ-ron: mạng tạo (generator) và mạng phân biệt (discriminator). Mạng tạo học cách tạo ra dữ liệu mới giống với dữ liệu thực tế, trong khi mạng phân biệt học cách phân biệt dữ liệu thực tế với dữ liệu do mạng tạo ra. GAN được sử dụng trong nhiều ứng dụng như tạo hình ảnh, tạo nhạc, dịch phong cách hình ảnh,…
Lợi ích của Deep Learning:
Tự động học tính năng một cách tự động.
Khám phá mẫu: Phân tích lượng lớn dữ liệu và khám phá các mẫu phức tạp trong hình ảnh, văn bản và âm thanh, đồng thời có thể rút ra những kết luận sâu sắc trong quá trình phân tích.
Xử lý các tập dữ liệu biến đổi nhanh: Phân loại và sắp xếp các tập dữ liệu có nhiều biến thể, chẳng hạn như trong hệ thống giao dịch và gian lận.
Xử lý cả dữ liệu có cấu trúc và không cấu trúc.
Bất kỳ node layer thêm vào nào được sử dụng đều hỗ trợ tối ưu hóa độ chính xác của các mô hình học sâu.
Thực hiện được nhiều tác vụ hơn các phương pháp học máy khác. Khi so sánh với các quy trình học máy thông thường, học sâu cần ít sự can thiệp của con người hơn và có thể phân tích dữ liệu mà các quy trình học máy khác không thể làm được.

Hạn chế của Deep Learning:
Chỉ biết những gì có trong dữ liệu mà con người đã đưa vào.
Nhiều thông tin sai lệch với thực tế.
Nếu tốc độ truyền dữ liệu đầu vào quá nhanh sẽ tạo ra giải pháp kém tối ưu. Ngược lại còn có thể bị đình trệ và thậm chí còn khó đạt được giải pháp hơn.
Cần có các bộ xử lý đồ họa hiệu suất cao đa lõi (GPU) và các bộ xử lý tương tự khác để đảm bảo cải thiện hiệu quả và giảm mức tiêu thụ thời gian.
Cần nhiều thiết bị đắt đắt tiền như RAM, ổ đĩa cứng hoặc ổ cứng thể rắn dựa trên RAM
Những hạn chế và thách thức khác bao gồm:
Yêu cầu số lượng lớn dữ liệu: Các mô hình deep learning yêu cầu lượng lớn dữ liệu để học, gây khó khăn cho việc áp dụng deep learning cho các vấn đề không có nhiều dữ liệu.
Thiếu tính đa nhiệm: Sau khi được đào tạo, các mô hình deep learning trở nên thiếu linh hoạt và không thể xử lý đa nhiệm. Chúng có thể đưa ra các giải pháp hiệu quả và chính xác nhưng chỉ cho một vấn đề cụ thể. Ngay cả việc giải quyết một vấn đề tương tự cũng sẽ yêu cầu đào tạo lại hệ thống.
Thiếu tính lý luận: Bất kỳ ứng dụng nào yêu cầu suy luận – chẳng hạn như lập trình hoặc áp dụng phương pháp khoa học – lập kế hoạch dài hạn và thao tác dữ liệu giống như thuật toán đều hoàn toàn vượt xa những gì các kỹ thuật học sâu hiện tại có thể làm được, ngay cả với lượng lớn dữ liệu.
Mạng Nơ-ron Tích chập (CNN - Convolutional Neural Network)

Hình 4: Convolutional neural network (CNN)
Khái niệm
Mạng Nơ-ron Tích chập (CNN) là một loại mạng học sâu (Deep Learning) được thiết kế đặc biệt để xử lý dữ liệu có dạng lưới hai chiều, chẳng hạn như hình ảnh.
Khác với các mạng nơ-ron khác (Fully Connected Neural Network, Incompletely Connected Neurol Network) — vốn xử lý từng điểm ảnh một cách riêng biệt — CNN có khả năng phát hiện và học tự động các đặc trưng không gian (spatial features) của hình ảnh như đường biên, góc cạnh, họa tiết hoặc hình dạng.
Trong hệ thống phân loại rác thải, CNN được sử dụng để “học” cách phân biệt giữa các loại vật thể như chai nhựa, lon kim loại, giấy, bìa cứng, thủy tinh, rác y tế, thiết bị điện tử... Tất cả được huấn luyện từ hàng ngàn ảnh đã gắn nhãn, giúp hệ thống có khả năng phân loại tự động rác thải trong thời gian thực.
Kiến trúc cơ bản của CNN
Một mô hình CNN thường gồm 5 loại lớp chính:
Lớp Convolution (Lớp tích chập): Là lớp tích chập là thành phần quan trọng nhất của CNN, chịu trách nhiệm trích xuất các đặc trưng từ dữ liệu đầu vào. Lớp này sử dụng một bộ lọc (kernel) - một ma trận nhỏ có kích thước phổ biến như 3x3 hoặc 5x5 - quét qua từng vùng nhỏ của hình ảnh và thực hiện phép nhân tích chập (convolution) giữa các giá trị pixel với trọng số của bộ lọc. Kết quả của quá trình này tạo thành bản đồ đặc trưng (feature map), giúp mô hình phát hiện các đặc điểm như cạnh, góc, màu sắc hoặc kết cấu trong ảnh.

Hình 5: Convolution Layer
Lớp Activation (Hàm kích hoạt – ReLU): Là lớp mà sau khi ta đã trích xuất ra các đặc trưng ra rồi thì sẽ sử dụng đến để lọc các đặc trưng để đầu ra là một ma trận với các số dương không âm để đưa vào xử lý ở các lớp sau.
ReLU=max⁡〖(0,x)〗

Hình 6: Hàm kích hoạt ReLU
Lớp Pooling (max pooling): Sau khi trích xuất đặc trưng qua lớp tích chập và hàm kích hoạt ReLU, CNN sử dụng Pooling Layer để giảm kích thước feature map, từ đó giảm số lượng tham số, tăng hiệu suất tính toán và tránh hiện tượng overfitting (mô hình học quá kỹ vào dữ liệu huấn luyện, nhưng lại hoạt động kém khi gặp dữ liệu mới). Pooling hoạt động bằng cách áp dụng một bộ lọc nhỏ (thường là 2x2 hoặc 3x3) để lấy giá trị đại diện cho mỗi vùng quét, giúp giữ lại những thông tin quan trọng nhất. Có hai phương pháp pooling phổ biến: Max Pooling và Average Pooling: Max Pooling, giá trị lớn nhất trong vùng quét sẽ được giữ lại, giúp mô hình tập trung vào những đặc trưng nổi bật nhất. Average Pooling tính trung bình các giá trị trong vùng quét, giúp tổng hợp thông tin thay vì chỉ giữ giá trị lớn nhất như Max Pooling.

Hình 7: Pooling Layer
Lớp Flatten (Làm phẳng): Để có thể đưa vào lớp cuối là lớp Fully Connected xử lý thì ta cần phải làm phẳng lại ma trận 2D thành vector 1D.

Hình 8: Flatten Layer (Làm phẳng)
Lớp Fully Connected (Dense Layer): là lớp kết nối đầy đủ nằm ở cuối mạng Convolutional Neural Networks, đóng vai trò tổng hợp tất cả các đặc trưng đã trích xuất và thực hiện nhiệm vụ phân loại hình ảnh. Ở lớp này, mỗi nơ-ron được kết nối với toàn bộ nơ-ron ở lớp trước, tạo nên một mạng lưới liên kết chặt chẽ. Các giá trị từ feature map trước đó sẽ được chuyển thành một vector một chiều, một chuỗi dài duy nhất và đưa vào lớp fully connected để xử lý. Quá trình này được gọi là Làm phẳng Flattening. Tiếp đó, CNN sử dụng các hàm kích hoạt phi tuyến như Softmax hoặc Sigmoid để tính toán xác suất cho từng lớp đầu ra. Điều này giúp cho mô hình đưa ra quyết định cuối cùng, chẳng hạn như phân loại hình ảnh thành các nhóm khác nhau (ví dụ: chó, mèo,...).

    Quá trình huấn luyện

Quá trình huấn luyện mô hình CNN bao gồm các bước:
Tiền xử lý dữ liệu: thay đổi kích thước ảnh (resize), chuẩn hóa pixel (normalization), tăng cường dữ liệu (data augmentation): xoay, lật, cắt, thay đổi sáng để mô hình học được tính đa dạng.
Lan truyền tuyến (Forward Propagation): ảnh đầu vào được truyền qua các lớp tích chập, kích hoạt, pooling và fully connected để sinh ra kết quả dự đoán.
Tính toán hàm mất mát (Loss Function): Đo độ sai lệch giữa nhãn thực tế và nhãn dự đoán.
Lan truyền ngược (Backpropagation): Tính đạo hàm và cập nhật trọng số trong quá trình huẩn luyện để giảm sai số dự đoán.
Huấn luyện lặp (Training Epochs): Quá trình lặp đi lặp lại quá trình huấn luyện qua các epochs cho đến khi đạt được độ chính xác mong muốn.
Ưu điểm và hạn chế
Ưu điểm:
Khả năng tự động trích xuất đặc trưng ảnh mà không cần xử lý thủ công.
Hiệu quả cao trong nhận dạng hình ảnh, đặc biệt là phân loại vật thể.
Tái sử dụng đặc trưng (Feature Reuse) giúp mô hình học sâu hơn và chính xác hơn.
Có thể ứng dụng cho dữ liệu thời gian thực (real-time image/video).
Hạn chế
Cần dữ liệu huấn luyện lớn và đa dạng để đạt kết quả tốt.
Thời gian huấn luyện dài, đòi hỏi GPU mạnh.
Hiệu suất giảm khi gặp ảnh bị nhiễu, ánh sáng kém hoặc góc nhìn phức tạp.
Các công nghệ sử dụng trong hệ thống
Hệ thống được phát triển dựa trên mô hình Mạng Nơ-ron Tích chập (CNN – Convolutional Neural Network), sử dụng kiến trúc MobileNetV2 trong TensorFlow/Keras để phân loại hình ảnh rác thải.
Bên cạnh đó, hệ thống còn tích hợp OpenCV trong quá trình xử lý ảnh đầu vào, Flask để triển khai mô hình dưới dạng dịch vụ web API, và SQL Server để lưu trữ dữ liệu kết quả phân loại.
Các công cụ hỗ trợ như Jupyter Notebook, Matplotlib, GitHub... được sử dụng nhằm hỗ trợ huấn luyện, đánh giá, và quản lý mô hình hiệu quả hơn.
TensorFlow / Keras
TensorFlow là một nền tảng học sâu (Deep Learning) mã nguồn mở do Google phát triển, được sử dụng rộng rãi trong việc xây dựng và huấn luyện các mô hình trí tuệ nhân tạo. Keras là một API cấp cao được tích hợp trong TensorFlow, giúp việc định nghĩa, huấn luyện và đánh giá mô hình trở nên nhanh chóng, dễ hiểu và dễ bảo trì.
Trong hệ thống này, TensorFlow/Keras đóng vai trò trung tâm trong việc huấn luyện mô hình phân loại hình ảnh rác thải. Nhờ khả năng xử lý song song trên GPU và hỗ trợ nhiều mô hình tiền huấn luyện (pretrained models), TensorFlow/Keras là lựa chọn tối ưu cho các bài toán thị giác máy tính (Computer Vision).
Thay vì xây dựng mô hình từ đầu (scratch), hệ thống sử dụng kỹ thuật Transfer Learning (Học chuyển giao) với kiến trúc nền tảng là MobileNetV2.
Cụ thể, mô hình MobileNetV2 – Đây là kiến trúc CNN được Google tối ưu hóa cho các thiết bị di động và nền tảng web với độ trễ thấp nhưng vẫn đảm bảo độ chính xác cao. Trong dự án, em sử dụng phiên bản đã được huấn luyện trước (pre-trained) trên tập dữ liệu ImageNet, loại bỏ lớp classification cuối cùng và thay thế bằng các lớp Fully Connected mới phù hợp với 7 loại rác thải của đề tài.
Cơ chế Fine-tuning: Các lớp tích chập ban đầu của MobileNetV2 được "đóng băng" (freeze) để giữ lại các đặc trưng cơ bản (cạnh, góc, màu sắc), chỉ huấn luyện lại các lớp cao hơn để nhận diện đặc trưng riêng biệt của rác thải.
Hàm mất mát tùy chỉnh (Custom Loss Function): Hệ thống không sử dụng hàm Cross-Entropy tiêu chuẩn mà áp dụng Focal Loss (với tham số gamma=1.0, alpha=0.25). Kỹ thuật này giúp mô hình tập trung học các mẫu khó phân loại và giải quyết vấn đề mất cân bằng dữ liệu giữa các loại rác phổ biến và hiếm gặp.
OpenCV (Open Source Computer Vision Library)
OpenCV là thư viện mã nguồn mở chuyên về xử lý ảnh và thị giác máy tính (Computer Vision), cung cấp hàng nghìn hàm hỗ trợ đọc, phân tích và thao tác với dữ liệu hình ảnh và video.
OpenCV đóng vai trò quan trọng trong việc tiền xử lý ảnh đầu vào và kết nối với camera thời gian thực, giúp chuyển đổi hình ảnh thu được từ thế giới thực thành dữ liệu đầu vào mà mô hình AI có thể hiểu và xử lý.
Cụ thể, Trước khi đưa vào mô hình AI, mọi hình ảnh từ Camera hoặc file tải lên đều được OpenCV xử lý qua các bước: Resize về kích thước chuẩn 224x224 pixel, chuyển đổi hệ màu từ BGR sang RGB, và chuẩn hóa giá trị pixel về khoảng [0, 1].
OpenCV truy xuất trực tiếp vào Webcam máy tính thông qua cv2.VideoCapture. Tại mỗi khung hình (frame), hệ thống thực hiện dự đoán và sử dụng các hàm đồ họa của OpenCV (cv2.rectangle, cv2.putText) để vẽ khung bao và hiển thị tên loại rác ngay trên màn hình video với độ trễ tối thiểu.
Trong hệ thống, OpenCV hoạt động như một cầu nối giữa phần cứng thu nhận dữ liệu (camera) và mô hình AI. Dữ liệu hình ảnh được OpenCV xử lý, chuyển đổi thành dạng ma trận, sau đó truyền vào mô hình TensorFlow để dự đoán. Kết quả phân loại được hiển thị lại cho người dùng hoặc gửi đến Flask API để lưu trữ và hiển thị trên giao diện web.
Flask (Python Web Framework)
Flask là một framework web nhẹ viết bằng ngôn ngữ Python, được sử dụng để phát triển các ứng dụng web hoặc dịch vụ API RESTful một cách nhanh chóng và linh hoạt. Trong hệ thống này, Flask đóng vai trò là nền tảng triển khai mô hình AI, giúp đưa mô hình học sâu đã được huấn luyện vào hoạt động thực tế.
Flask-RESTful: Xây dựng các Endpoint như /predict (dự đoán), /auth/login (đăng nhập) tuân thủ chuẩn HTTP.
Flask-JWT-Extended: Đảm bảo bảo mật cho hệ thống thông qua cơ chế xác thực bằng JSON Web Token (JWT). Mỗi khi User đăng nhập thành công, Server cấp một Token mã hóa, Client cần đính kèm Token này trong Header của các request tiếp theo để được phép truy cập tài nguyên.
CORS (Cross-Origin Resource Sharing): Sử dụng flask-cors để cho phép giao diện Frontend (chạy trên trình duyệt) có thể gọi API từ Backend một cách hợp lệ.
SQL Server (Cơ sở dữ liệu quan hệ)
Hệ thống sử dụng Microsoft SQL Server làm nơi lưu trữ dữ liệu bền vững, được quản lý thông qua SQLAlchemy ORM (Object Relational Mapping).
SQLAlchemy ORM: Thay vì viết các câu lệnh SQL thuần túy dễ gây lỗi, dự án sử dụng SQLAlchemy để thao tác với SQL Server thông qua các đối tượng Python (Class). Các bảng dữ liệu được định nghĩa dưới dạng Class trong models.py (Ví dụ: class User(db.Model), class ClassificationResult(db.Model)).
Thiết kế dữ liệu:
Bảng roles: Lưu trữ nhóm các quyền hạn trong hệ thống.
Bảng users: Lưu trữ thông tin định danh và vai trò (Role) của người dùng.
Bảng images & classification_results: Lưu trữ đường dẫn ảnh và kết quả phân loại (nhãn, độ tin cậy) phục vụ cho việc thống kê lịch sử.
Bảng waste_types: Lưu trữ thông tin về các loại rác mà mô hình AI có thể nhận diện (7 loại: Cardboard, Glass, Plastic...).
Bảng feedbacks: Thu thập phản hồi đúng/sai từ người dùng để làm dữ liệu huấn luyện lại mô hình trong tương lai.
Công cụ hỗ trợ khác (tùy chọn)
Bên cạnh các công nghệ chính nêu trên, hệ thống còn sử dụng một số công cụ hỗ trợ nhằm tối ưu quy trình phát triển và huấn luyện mô hình.
Jupyter Notebook và Google Colab là hai môi trường lập trình tương tác thuận tiện cho việc xây dựng, kiểm thử và huấn luyện mô hình AI.
Các thư viện trực quan hóa như Matplotlib và Seaborn được sử dụng để biểu diễn các biểu đồ huấn luyện như độ chính xác (accuracy) và sai số (loss) qua từng epoch, giúp đánh giá trực quan hiệu quả của mô hình.
Ngoài ra, các kỹ thuật như ModelCheckpoint và EarlyStopping trong Keras giúp mô hình tự động lưu phiên bản tốt nhất và dừng huấn luyện sớm khi đạt ngưỡng tối ưu.
Cuối cùng, Git và GitHub được dùng để quản lý mã nguồn, theo dõi thay đổi và đảm bảo tính nhất quán trong phát triển phần mềm.

Phần III. PHÂN TÍCH HỆ THỐNG
Tổng quan về hệ thống
Hệ thống "Nhận diện và phân loại rác thải" được xây dựng nhằm giải quyết bài toán tự động hóa trong việc phân loại rác tại nguồn. Hệ thống hoạt động dựa trên sự kết hợp chặt chẽ giữa hai quy trình chính:
Quy trình Huấn luyện (Offline): Thực hiện thu thập dữ liệu, gán nhãn và huấn luyện mô hình Deep Learning (sử dụng kiến trúc MobileNetV2) trên máy chủ có cấu hình GPU mạnh. Kết quả đầu ra là tệp trọng số mô hình (.h5) có khả năng nhận diện 7 loại rác thải.
Quy trình Vận hành (Online): Triển khai mô hình đã huấn luyện lên ứng dụng Web. Người dùng tương tác thông qua giao diện để tải ảnh hoặc sử dụng Camera. Hệ thống xử lý ảnh bằng OpenCV, đưa qua mô hình phân loại và trả về kết quả thời gian thực.
Hai giai đoạn này liên kết với nhau theo một chu trình khép kín: dữ liệu -> huấn luyện -> mô hình -> triển khai -> phản hồi từ người dùng -> tái huần luyện.
Phân tích yêu cầu
Giai đoạn huấn luyện
Đây là giai đoạn thực hiện trên máy trạm của nhà phát triển, không yêu cầu kết nối Internet liên tục hay tương tác với người dùng cuối.
Yêu cầu về Dữ liệu:
Hệ thống cần thu thập và chuẩn hóa bộ dữ liệu rác thải (từ nguồn TrashNet và ảnh thực tế) bao gồm 7 nhãn: Cardboard, Glass, Metal, Paper, Plastic, E-waste, Medical.
Thực hiện gán nhãn (Labeling) thủ công chính xác cho từng ảnh.
Thực hiện kỹ thuật Tăng cường dữ liệu (Data Augmentation): Xoay, lật, zoom, chỉnh sáng để làm phong phú dữ liệu huấn luyện, giúp mô hình tránh hiện tượng học vẹt (Overfitting).

Yêu cầu về Mô hình AI (Core Engine):
Xây dựng mô hình Mạng nơ-ron tích chập (CNN) dựa trên kiến trúc MobileNetV2 (Transfer Learning) để tối ưu hóa giữa độ chính xác và tốc độ xử lý.
Đầu vào: Ảnh màu kích thước chuẩn 224x224 pixel.
Đầu ra: Vector xác suất tương ứng với 7 loại rác.
Hàm mất mát: Sử dụng Focal Loss để xử lý vấn đề mất cân bằng dữ liệu (ví dụ: ảnh nhựa nhiều hơn ảnh rác y tế).
Yêu cầu đầu ra (Output):
Tệp trọng số mô hình (.h5 hoặc SavedModel) có khả năng tái sử dụng.
Độ chính xác (Accuracy) trên tập kiểm thử (Test set) phải đạt tối thiểu 80%.
Giai đoạn triển khai hệ thống
Giai đoạn này tập trung vào việc đưa mô hình CNN đã được huấn luyện (file .h5) vào một ứng dụng thực tế, cho phép người dùng cuối tương tác và nhận kết quả phân loại. Các yêu cầu cho giai đoạn này bao gồm việc xây dựng API backend, giao diện người dùng và cơ sở dữ liệu.
Yêu cầu chức năng cho Người dùng (End-User):
Upload ảnh phân loại: Người dùng tải ảnh tĩnh (.jpg, .png) lên hệ thống. Server xử lý và trả về kết quả dự đoán kèm độ tin cậy.
Phân loại Real-time (Camera): Hệ thống kết nối trực tiếp với Webcam/Camera của thiết bị; Sử dụng OpenCV để bắt luồng video, cắt khung hình (Frame) và gửi vào mô hình phân loại; Kết quả (Tên rác + Khung bao) được vẽ trực tiếp lên màn hình video với độ trễ thấp.
Đăng ký & Đăng nhập: Cho phép người dùng tạo tài khoản cá nhân để lưu trữ lịch sử hoạt động (Sử dụng JWT Token để bảo mật phiên làm việc).
Quản lý lịch sử: Người dùng xem lại danh sách các lần phân loại trước đó.
Gửi phản hồi (Feedback): Người dùng có thể báo cáo "Sai" hoặc "Đúng" đối với kết quả AI trả về để đóng góp dữ liệu cho hệ thống.
Yêu cầu chức năng cho Quản trị viên (Admin):
Dashboard thống kê: Hiển thị tổng quan số lượng rác đã phân loại, biểu đồ tỷ lệ các loại rác (Ví dụ: Nhựa chiếm 40%, Giấy 20%...) dựa trên dữ liệu từ SQL Server.
Quản lý người dùng: Xem danh sách User, tìm kiếm và khóa (Block) các tài khoản vi phạm.
Quản lý danh mục rác (Waste Types): Cập nhật thông tin hướng dẫn tái chế, mã màu sắc hiển thị cho từng loại rác mà không cần can thiệp vào code.
Quản lý phản hồi: Duyệt các phản hồi từ người dùng để lọc ra bộ dữ liệu "khó" nhằm huấn luyện lại mô hình trong tương lai.
Yêu cầu phi chức năng (Non-functional):
Khả năng mở rộng: Hệ thống Backend (Flask) và Database (SQL Server) thiết kế theo mô hình 3 lớp, dễ dàng mở rộng thêm tính năng mới.
Bảo mật: Mật khẩu người dùng được mã hóa (Hashing); API được bảo vệ chống truy cập trái phép.
Hiệu năng (Performance): Tốc độ phản hồi API (Latency): Dưới 2 giây cho tác vụ upload ảnh; Tốc độ khung hình (FPS) cho Real-time: Đạt tối thiểu 10-15 FPS để đảm bảo trải nghiệm mượt mà.
Phân tích và thiết kế hệ thống
Thiết kế kiến trúc tổng quan (System Architecture)
Hệ thống được thiết kế theo kiến trúc Client-Server (3 lớp) để đảm bảo tính linh hoạt, dễ bảo trì và mở rộng.
Client (Lớp giao diện): Là một ứng dụng web đơn giản (sử dụng HTML/CSS/JS) . Giao diện này cho phép người dùng tương tác, tải ảnh tĩnh lên hoặc sử dụng webcam để thu nhận hình ảnh thời gian thực.
Application Layer (Lớp ứng dụng): Sử dụng Flask làm API backend. Máy chủ này đóng vai trò trung tâm, có nhiệm vụ: Tiếp nhận các yêu cầu HTTP (chứa dữ liệu hình ảnh) từ Client; Sử dụng OpenCV để tiền xử lý ảnh đầu vào (thay đổi kích thước về 224x224, chuẩn hóa pixel); Tải mô hình TensorFlow/Keras (tệp .h5) đã được huấn luyện để thực hiện dự đoán (inference); Ghi lại kết quả phân loại (loại rác, độ tin cậy, thời gian) vào cơ sở dữ liệu; Trả kết quả dự đoán (thường ở dạng JSON) về cho Client.
Database (Lớp dữ liệu): Sử dụng Hệ quản trị SQL Server để lưu trữ dữ liệu có cấu trúc, bao gồm thông tin người dùng, danh mục các loại rác, lịch sử phân loại và phản hồi.
Phân tích các Use Case

    Thiết kế luồng hoạt động (Activity Flow)

Luồng Phân loại ảnh (Upload):
Người dùng chọn ảnh từ thiết bị -> Client gửi POST /api/classify kèm file ảnh.
Server lưu ảnh vào thư mục tạm -> Ghi nhận vào bảng images.
ClassificationService đọc ảnh -> Resize về 224x224 -> Chuẩn hóa [0,1].
Mô hình AI dự đoán -> Trả về vector xác suất -> Chọn nhãn có xác suất cao nhất (Argmax).
Server lưu kết quả vào bảng classification_results -> Trả JSON về Client.
Client hiển thị ảnh kèm tên loại rác và độ tin cậy.
Luồng Phân loại Real-time (Camera):
Client mở Webcam -> Chụp liên tục các khung hình (Frame) với tốc độ quy định (ví dụ: 500ms/frame).
Client mã hóa Frame dưới dạng Base64/Blob -> Gửi về API.
Server nhận Frame -> Sử dụng OpenCV xử lý tiền kỳ -> Đưa vào mô hình AI.
Server trả về kết quả ngay lập tức (Low latency).
Client nhận kết quả -> Vẽ khung (Bounding Box) và tên rác chồng lên Video đang phát.
Luồng Huấn luyện lại (Retrain - Offline):
Admin lọc các bản ghi trong bảng feedbacks có feedback_type = 'incorrect'.
Trích xuất các ảnh tương ứng từ bảng images để gán lại nhãn đúng.
Thêm các ảnh này vào tập Dataset huấn luyện.
Chạy lại quy trình Train trên máy Server -> Tạo ra file model phiên bản mới (ví dụ: v1.1).
Cập nhật file .h5 mới vào hệ thống Backend.
Thiết kế cơ sở dữ liệu (Database)
Bảng roles:

Hình 9: Bảng roles

    Bảng users:

Hình 10: Bảng users

    Bảng images:

Hình 11: Bảng images

    Bảng waste_types:

Hình 12: Bảng waste_types

    Bảng classification_results:

Hình 13: Bảng classification_results

    Bảnh feedbacks:

Hình 14: Bảng feedbacks

    Quan hệ giữa các bảng:

Hình 15: DB Relationship

Phần IV. THIẾT KẾ VÀ XÂY DỰNG HỆ THỐNG
Môi trường phát triển
Để xây dựng hệ thống, dự án sử dụng các môi trường và công cụ lập trình sau:
Ngôn ngữ lập trình: Python 3.11 (Backend & AI), JavaScript (Frontend).
IDE (Môi trường phát triển tích hợp): Visual Studio Code.
Quản lý mã nguồn: Git & GitHub.
Cơ sở dữ liệu: Microsoft SQL Server (Quản lý bằng SQL Server Management Studio - SSMS).
Công cụ kiểm thử API: Postman.
Thư viện chính: Backend bao gồm Flask, Flask-SQLAlchemy, Flask-JWT-Extended, PyODBC; AI & Xử lý ảnh bao gồm TensorFlow 2.12, OpenCV-Python, NumPy, Pillow.
Xây dựng Module AI và xử lý ảnh
Cấu hình và tải mô hình (Model loading)
Hệ thống sử dụng cơ chế Lazy Loading (tải trễ) để tối ưu hóa tài nguyên. Mô hình chỉ được tải vào bộ nhớ RAM khi có yêu cầu dự đoán đầu tiên. File xử lý chính: api/services/classification_service.py.
Load Model: Sử dụng tf.keras.models.load_model để tải file trọng số .h5.
Custom Objects: Khi tải mô hình, hệ thống cần đăng ký hàm mất mát tùy chỉnh focal_loss để TensorFlow có thể tái tạo lại kiến trúc mạng đã huấn luyện.
(trích code)
Tiền xử lý ảnh (Preprocessing)
Trước khi đưa vào mô hình, ảnh từ người dùng (Upload hoặc Camera) phải được chuẩn hóa đồng bộ với dữ liệu huấn luyện.
Resize: Đưa ảnh về kích thước cố định 224x224 pixel.
Color Space: Chuyển đổi không gian màu sang RGB (nếu ảnh gốc là RGBA hoặc Grayscale).
Normalization: Chia giá trị pixel cho 255.0 để đưa về khoảng [0, 1].
Batching: Thêm chiều batch (expand_dims) để tạo tensor có shape (1, 224, 224, 3).
Xây dựng Backend API
Kiến trúc phần mềm và tổ chức mã nguồn
Để đảm bảo tính mở rộng (Scalability) và dễ bảo trì (Maintainability), mã nguồn Backend được tổ chức theo mô hình MVC (Model-View-Controller) biến thể cho API (Model-Route-Service):
Tầng Route (Controller): (api/routes/) Chỉ chịu trách nhiệm tiếp nhận HTTP Request, validate dữ liệu đầu vào và trả về HTTP Response. Không chứa logic nghiệp vụ phức tạp.
Tầng Service (Business Logic): (api/services/) Chứa toàn bộ logic xử lý nghiệp vụ (ví dụ: xử lý ảnh, gọi thuật toán AI, tính toán thống kê).
Tầng Model (Data Access): (api/models.py) Định nghĩa cấu trúc dữ liệu và tương tác trực tiếp với SQL Server thông qua ORM.
Việc đăng ký các phân hệ (Module) được thực hiện thông qua cơ chế Flask Blueprints trong file api/routes/**init**.py. Điều này cho phép nhóm các API cùng chức năng lại với nhau (ví dụ: nhóm Auth, nhóm User, nhóm Classification).
Cấu hình hệ thống và kết nối cơ sở dữ liệu
Cấu hình hệ thống được quản lý tập trung tại file api/config.py, sử dụng biến môi trường .env (Environment Variables) để bảo mật các thông tin nhạy cảm.
Cơ chế kết nối: Sử dụng thư viện SQLAlchemy kết hợp với driver PyODBC để kết nối tới Microsoft SQL Server.
Connection String: Chuỗi kết nối được cấu trúc theo định dạng chuẩn: mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server
ORM Mapping: Các bảng dữ liệu được ánh xạ thành các Class Python (kế thừa từ db.Model). Hệ thống sử dụng cơ chế db.create_all() trong file khởi chạy app.py để tự động đồng bộ hóa cấu trúc bảng vào database nếu chưa tồn tại.
Cơ chế Xác thực và Bảo mật (Authentication & Security)
Bảo mật là ưu tiên hàng đầu trong tài liệu kỹ thuật này. Hệ thống triển khai các biện pháp sau trong api/routes/auth_routes.py:
Mã hóa mật khẩu (Password Hashing): Sử dụng thuật toán PBKDF2 (thông qua werkzeug.security.generate_password_hash) để băm mật khẩu trước khi lưu vào database. Tuyệt đối không lưu mật khẩu dạng văn bản thuần (plain text). Khi đăng nhập, hệ thống so khớp mật khẩu người dùng nhập vào với chuỗi hash trong DB bằng check_password_hash.
Cơ chế JWT (JSON Web Token): Sử dụng thư viện Flask-JWT-Extended để quản lý phiên làm việc. Quy trình cấp Token: Khi đăng nhập thành công (/api/auth/login), Server ký và cấp một access_token chứa thông tin định danh (sub=user_id) và thời gian hết hạn (ví dụ: 24 giờ). Bảo vệ API: Các API nhạy cảm (như gửi Feedback, xem thông tin User) được bảo vệ bằng Decorator @jwt_required(). Client phải gửi token này trong header Authorization: Bearer <token> để được truy cập.
Xử lý Logic Nghiệp vụ (Business Logic Implementation)
Logic Phân loại ảnh (Classification Flow):
Quy trình xử lý tại API POST /api/classify/predict được thiết kế chặt chẽ để đảm bảo hiệu năng và độ tin cậy:
Validation: Kiểm tra định dạng file (chỉ chấp nhận .jpg, .png, .jpeg) và kích thước file.
Lưu trữ file: File ảnh được đổi tên bằng mã UUID (Universally Unique Identifier) để tránh trùng lặp tên, sau đó lưu vào thư mục uploads/.
Xử lý AI: Gọi hàm classification_service.predict(image_path). Hàm này thực hiện: Tiền xử lý ảnh (Resize 224x224, Normalize); Chạy mô hình MobileNetV2 để lấy vector xác suất; Xác định nhãn có xác suất cao nhất (Max Confidence).
Transaction: Sử dụng SQL Transaction để ghi nhận kết quả vào bảng ClassificationResult và Image cùng lúc. Nếu có lỗi xảy ra, toàn bộ thao tác sẽ được Rollback để đảm bảo toàn vẹn dữ liệu.
Logic Quản lý người dùng và Phản hồi:
API User (/api/users): Cung cấp các phương thức CRUD (Create, Read, Update, Delete) cho Admin. Logic lọc danh sách user cho phép phân trang (Pagination) và tìm kiếm theo tên/email.
API Feedback (/api/feedback): Cho phép người dùng gửi đánh giá về kết quả phân loại. Dữ liệu này được lưu kèm với classification_id để kỹ sư có thể truy xuất lại bức ảnh gốc và nhãn dự đoán, phục vụ việc gán nhãn lại (Re-labeling).
Xử lý lỗi và Logging (Error Handling)
Để đảm bảo tính ổn định và khả năng debug, hệ thống áp dụng cơ chế xử lý lỗi tập trung:
Try-Except Blocks: Mọi logic tương tác với File IO hoặc Database đều được bao bọc trong khối try-except.
HTTP Status Codes: API trả về mã lỗi chuẩn HTTP: 200 OK - Thành công; 400 Bad Request - Dữ liệu đầu vào sai (thiếu ảnh, sai định dạng); 401 Unauthorized - Chưa đăng nhập hoặc Token hết hạn; 500 Internal Server Error - Lỗi hệ thống (kèm theo log chi tiết bên phía server để debug).
Logging: Hệ thống ghi log các sự kiện quan trọng (Model loaded, Prediction error) ra Console hoặc File log để theo dõi sức khỏe hệ thống.
Xây dựng Frontend
Giao diện chương trình
