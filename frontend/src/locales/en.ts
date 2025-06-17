export default {
  common: {
    close: 'Close',
    loading: 'Loading...',
    home: 'Home',
    select: 'Select',
    characters: 'characters',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    edit: 'Edit',
    search: 'Search',
    back: 'Back',
    next: 'Next',
    previous: 'Previous',
    remove: 'Remove'
  },
  nav: {
    collections: 'Collection',
    selectCollection: 'Select Collection',
    dashboard: 'Dashboard',
    settings: 'Settings',
    newChat: 'New Chat',
    recentChat: 'Recent Chat',
    showLess: 'Show Less',
    showMore: 'Show More'
  },
  chat: {
    greeting: 'Hi there!',
    subtitle: 'What can I help you today?',
    inputPlaceholder: 'Input your question here',
    inputPlaceholderWithFile: 'Ask a question about the attached PDF...',
    user: 'User',
    aiAssistant: 'AI Assistant',
    lastResponseTime: 'Last response time:',
    appName: 'RAG Expert Chat',
    model: 'Model',
    selectModel: 'Select Model',
    selectModelPlaceholder: 'Select Model',
    fileUpload: {
      dragDropTitle: 'Drop your PDF files here',
      dragDropSubtitle: 'to add them to your conversation',
      supportedFormats: 'PDF files only • Max size: 10MB',
      fileAttached: 'File Attached',
      fileAttachedDetail: 'added to your conversation',
      fileRemoved: 'File Removed',
      fileRemovedDetail: 'PDF attachment removed',
      invalidFileType: 'Invalid File Type',
      invalidFileTypeDetail: 'Only PDF files are allowed',
      fileTooLarge: 'File Too Large',
      fileTooLargeDetail: 'File size must be less than 10MB',
      onlyPdfSupported: 'Only PDF files are supported',
      attachPdfFile: 'Attach PDF file'
    }
  },
  translate: {
    title: 'Translate',
    language: 'Language',
    placeholder: 'Enter text to translate...',
    targetLanguage: 'Target Language',
    sourceLanguage: 'Source Language',
    tones: {
      neutral: 'Neutral',
      formal: 'Formal',
      professional: 'Professional',
      informal: 'Informal',
      friendly: 'Friendly'
    }
  },
  compare: {
    title: 'Compare Documents',
    subtitle: 'Compare two documents to identify differences and similarities',
    analysisMode: 'Analysis Mode',
    document1: 'Document 1',
    document2: 'Document 2',
    dropFileHere: 'Drop file here or click to browse',
    supportedFormats: 'PDF, TXT, DOC, DOCX, or MD files',
    generateComparison: 'Generate Comparison',
    generatingComparison: 'Generating Comparison...',
    analyzing: 'Analyzing documents and generating comparison...',
    clickToStart: 'Click to start comparing',
    modes: {
      technical: 'Technical',
      compliance: 'Compliance',
      differences: 'Differences',
      similarities: 'Similarities'
    },
    errors: {
      invalidFileType: 'Invalid File Type',
      invalidFileTypeDetail: 'Please upload PDF, TXT, DOC, DOCX, or MD files only.',
      missingFiles: 'Missing Files',
      missingFilesDetail: 'Please upload both files before generating comparison.',
      noModelSelected: 'No Model Selected',
      noModelSelectedDetail: 'Please select a model first.',
      noCollectionSelected: 'No Collection Selected',
      noCollectionSelectedDetail: 'Please select a collection first.',
      comparisonFailed: 'Comparison Failed',
      comparisonFailedDetail: 'Failed to generate comparison. Please try again.'
    },
    noResults: 'No results to display yet. Upload files and click generate to start comparing.'
  },
  messages: {
    noCollectionsFound: 'No Collections Found',
    noModelsFound: 'No Models Found',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Information'
  },
  buttons: {
    submit: 'Submit',
    reset: 'Reset',
    confirm: 'Confirm',
    retry: 'Retry'
  },
  forms: {
    required: 'This field is required',
    invalidEmail: 'Please enter a valid email',
    invalidFormat: 'Invalid format'
  },
  modals: {
    selectModel: 'Select Model',
    searchModels: 'Search models...',
    searchCollections: 'Search collections...'
  },
  codeBlock: {
    defaultLanguage: 'text',
    copy: 'Copy code',
    copied: 'Copied!'
  },
  streaming: {
    thinking: 'Thinking...',
    thinkingProcess: 'Thinking Process',
    thinkingInProgress: 'Thinking in progress...',
    processingQuery: 'Processing your query...',
    ragSystemWorking: 'RAG system is working',
    analyzingQuery: 'Analyzing query and retrieving relevant documents',
    processingContext: 'Processing context with AI model',
    generatingResponse: 'Generating response...',
    noContent: 'No content',
    sources: 'Sources',
    copied: 'Copied!'
  }
}