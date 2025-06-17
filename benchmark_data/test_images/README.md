# Test Data Structure

Your test images should be organized as follows:

```
test_images/
├── person1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
├── person2/
│   ├── image1.jpg
│   └── image2.jpg
├── person3/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
└── ...
```

## Guidelines:
- Each person should have their own directory
- Each person should have at least 2 images for genuine pair testing
- Use clear, front-facing photos when possible
- Supported formats: .jpg, .png
- Minimum 3 different people recommended
- 5-10 people with 3-5 images each is ideal for comprehensive testing

## Preparing Your Data:
1. Create directories named after each person (e.g., person1, person2, etc.)
2. Place multiple images of the same person in their respective directory
3. Ensure good image quality and proper face visibility
4. The benchmark will automatically create genuine pairs (same person) and impostor pairs (different people)