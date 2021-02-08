model_path = r"C:\Users\zayon\Documents\MSC\NN\project\experiments\exp_3_y\face_landmarks.pth"
images_path = r"C:\Users\zayon\Documents\MSC\NN\project\datasets\images_yonit"


class NetworkResnet18(nn.Module):
    def __init__(self, num_classes=98 * 2):
        super().__init__()
        self.model_name = 'resnet18'
        self.model = models.resnet18()
        # self.model.conv1=nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        x = self.model(x)
        return x


class NetworkResnet50(nn.Module):
    def __init__(self, num_classes=98 * 2, pretrained=False):
        super().__init__()
        self.model_name = 'resnet50'
        if pretrained:
            self.model = models.resnet50(pretrained=True)
            for param in self.model.parameters():
                param.requires_grad = False
        else:
            self.model = models.resnet50()
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x):
        x = self.model(x)
        return x


def NME(preds, ground_true, d_type="eyes", half=False):
  nme = []
  for pred, label in zip(preds, ground_true):
    if d_type == "eyes":
      left_eye = (label[60]+label[64])/2
      right_eye = (label[68]+label[72])/2
      d = torch.sqrt(torch.sum(torch.square(left_eye-right_eye)))
    else:
      d = 1
    _nme = torch.norm(pred - label)

    if half:
      polynomial = compute_line(label.numpy()[[51, 79]])
      idx = np.array([i for i, v in enumerate(label) if v[1] < polynomial(v[0])])
      _nme = torch.norm(pred[idx] - label[idx])

    _nme = _nme/d
    nme.append(_nme)
  return np.mean(nme)


best_network = NetworkResnet50()
best_network.cuda()
best_network.load_state_dict(torch.load('/content/face_landmarks.pth'))
def evaluate_model(test_loader, model, visualize=True):
  model = model.cuda()
  start_time = time.time()
  full_error = []
  half_error = []
  test_it = iter(test_loader)
  # for samples in test_loader:
  with torch.no_grad():
    model.eval()
    for step in range(1,len(test_loader)+1):
      samples = next(test_it)
      images, landmarks = samples['images'], samples['landmarks']
      images = images.cuda()
      landmarks = (landmarks + 0.5) * 224

      predictions = (model(images).cpu() + 0.5) * 224
      predictions = predictions.view(-1,98,2)

      full_error.append(NME(predictions, landmarks))
      # half_error.append(NME(predictions, landmarks, half=True))
      if visualize:
        plt.figure(figsize=(10,40))
        for img_num in range(8):
            plt.subplot(8,1,img_num+1)
            image = images[img_num].cpu().permute(1, 2, 0)
            plt.imshow(image)
            # plt.imshow(cv2.cvtColor(images[img_num].cpu().numpy().transpose(1,2,0).squeeze(), cv2.COLOR_BGR2RGB) )
            plt.scatter(predictions[img_num,:,0], predictions[img_num,:,1], c = 'r', s = 5)
            plt.scatter(landmarks[img_num,:,0], landmarks[img_num,:,1], c = 'g', s = 5)
      visualize = False
  # print('Total number of test images: {}'.format(len(test_loader.dataset)))

  # end_time = time.time()
  # print("Elapsed Time : {}".format(end_time - start_time))
    Full_error = np.mean(full_error)
    # Half_error = np.mean(half_error)
  # print("Full error: ", np.mean(full_error))
  # print("Half error: ", np.mean(half_error))
    return Full_error

print(evaluate_model(test_loader, best_network, visualize=True))