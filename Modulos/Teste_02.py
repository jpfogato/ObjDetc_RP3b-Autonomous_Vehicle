# Neste modulo e feita a:
# Selecao da camera: PiCam
# Identificacao do modelo utilizado

#seleciona a camera a ser utilizada
camera_type = 'picamera'

#identifica o modelo
MODEL_NAME = 'placas_model'

#pega o PATH do diretorio atual de trabalho
CWD_PATH = os.getcwd()

# PATH do inferece_graph (.pb) que contem o modelo utilizado para deteccao de objetos
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# PATH para o arquivo de label map
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','placas_labelmap.pbtxt')

# Numero de classes detectaveis
NUM_CLASSES = 3

## Carregando o Labelmap
# O indice do labelmap relaciona com um nome de categoria, entao quando a rede
# convolucional preve um '1', sabemos que isso corresponde a placa de 'pare'.

# carrega o labelmap dentro da variavel 'label_map'
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

# converte os labelmaps em categorias e adiciona a variavel 'categories'
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)

# cria um indice de categorias baseado na variavel 'categories'
category_index = label_map_util.create_category_index(categories)

# carrega o modelo do TensorFlow para a memoria
with tf.Graph().as_default() #wrapper que compatibiliza com TF2.0
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

# Define os Tensores de entrada e saida (dados) para o classificador

# Tensor de entrada e a imagem
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Os tensores de saida sao as caixas de deteccao, scores e classes
# Cada caixa representa uma parte da imagem onde um objeto foi detectado
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# O score representa o nivel de confianca para cada objeto
# O score e apresentado na imagem resultante, junto com um label da classe
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Numero de objetos detectados
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Inicializa a calculadora de framerate
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Inicializa a camera e inicia a deteccao de objetos

if camera_type == 'picamera':
    # Inicializa a PiCam e pega a referencia para os dados da captura
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # # Draw the results of the detection (aka 'visulaize the results')
        # vis_util.visualize_boxes_and_labels_on_image_array(
        #     frame,
        #     np.squeeze(boxes),
        #     np.squeeze(classes).astype(np.int32),
        #     np.squeeze(scores),
        #     category_index,
        #     use_normalized_coordinates=True,
        #     line_thickness=8,
        #     min_score_thresh=0.40)
        #
        # cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        #
        # # All the results have been drawn on the frame, so it's time to display it.
        # cv2.imshow('Object detector', frame)
        #
        # t2 = cv2.getTickCount()
        # time1 = (t2-t1)/freq
        # frame_rate_calc = 1/time1
        #
        # # Press 'q' to quit
        # if cv2.waitKey(1) == ord('q'):
        #     break

        rawCapture.truncate(0)

    camera.close()
