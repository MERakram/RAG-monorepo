export default {
  common: {
    close: 'Fermer',
    loading: 'Chargement...',
    home: 'Accueil',
    select: 'Sélectionner',
    characters: 'caractères',
    save: 'Enregistrer',
    cancel: 'Annuler',
    delete: 'Supprimer',
    edit: 'Modifier',
    search: 'Rechercher',
    back: 'Retour',
    next: 'Suivant',
    previous: 'Précédent',
    remove: 'Supprimer'
  },
  nav: {
    normes: 'Norme',
    selectNorme: 'Sélectionner une Norme',
    dashboard: 'Tableau de bord',
    settings: 'Paramètres',
    newChat: 'Nouveau Chat',
    recentChat: 'Chat Récent',
    showLess: 'Afficher Moins',
    showMore: 'Afficher Plus'
  },
  chat: {
    greeting: 'Bonjour !',
    subtitle: 'Que puis-je vous aider aujourd\'hui ?',
    inputPlaceholder: 'Saisissez votre question ici',
    inputPlaceholderWithFile: 'Posez une question sur le PDF attaché...',
    user: 'Utilisateur',
    aiAssistant: 'Assistant IA',
    lastResponseTime: 'Temps de réponse :',
    appName: 'CA-NormExpert Chat',
    model: 'Modèle',
    selectModel: 'Sélectionner un Modèle',
    selectModelPlaceholder: 'Sélectionner un Modèle',
    fileUpload: {
      dragDropTitle: 'Déposez vos fichiers PDF ici',
      dragDropSubtitle: 'pour les ajouter à votre conversation',
      supportedFormats: 'Fichiers PDF uniquement • Taille max: 10MB',
      fileAttached: 'Fichier attaché',
      fileAttachedDetail: 'ajouté à votre conversation',
      fileRemoved: 'Fichier supprimé',
      fileRemovedDetail: 'Pièce jointe PDF supprimée',
      invalidFileType: 'Type de fichier invalide',
      invalidFileTypeDetail: 'Seuls les fichiers PDF sont autorisés',
      fileTooLarge: 'Fichier trop volumineux',
      fileTooLargeDetail: 'La taille du fichier doit être inférieure à 10MB',
      onlyPdfSupported: 'Seuls les fichiers PDF sont pris en charge',
      attachPdfFile: 'Joindre un fichier PDF'
    }
  },
  translate: {
    title: 'Traduire',
    language: 'Langue',
    placeholder: 'Entrez le texte à traduire...',
    targetLanguage: 'Langue cible',
    sourceLanguage: 'Langue source',
    tones: {
      neutral: 'Neutre',
      formal: 'Formel',
      professional: 'Professionnel',
      informal: 'Informel',
      friendly: 'Amical'
    }
  },
  compare: {
    title: 'Comparer les Normes',
    subtitle: 'Comparer deux fichiers de normes électriques',
    analysisMode: 'Mode d\'Analyse',
    standard1: 'Norme 1',
    standard2: 'Norme 2',
    dropFileHere: 'Déposez le fichier ici ou cliquez pour parcourir',
    supportedFormats: 'Fichiers PDF, TXT, DOC, DOCX ou MD',
    generateComparison: 'Générer la Comparaison',
    generatingComparison: 'Génération de la Comparaison...',
    analyzing: 'Analyse des normes et génération de la comparaison...',
    clickToStart: 'Cliquez pour commencer à comparer',
    modes: {
      technical: 'Technique',
      compliance: 'Conformité',
      differences: 'Différences',
      similarities: 'Similitudes'
    },
    errors: {
      invalidFileType: 'Type de Fichier Invalide',
      invalidFileTypeDetail: 'Veuillez télécharger uniquement des fichiers PDF, TXT, DOC, DOCX ou MD.',
      missingFiles: 'Fichiers Manquants',
      missingFilesDetail: 'Veuillez télécharger les deux fichiers avant de générer la comparaison.',
      noModelSelected: 'Aucun Modèle Sélectionné',
      noModelSelectedDetail: 'Veuillez d\'abord sélectionner un modèle.',
      noCollectionSelected: 'Aucune Collection Sélectionnée',
      noCollectionSelectedDetail: 'Veuillez d\'abord sélectionner une collection.',
      comparisonFailed: 'Échec de la Comparaison',
      comparisonFailedDetail: 'Impossible de générer la comparaison. Veuillez réessayer.'
    },
    noResults: 'Aucun résultat à afficher pour le moment. Téléchargez des fichiers et cliquez sur générer pour commencer la comparaison.'
  },
  messages: {
    noNormesFound: 'Aucune Norme Trouvée',
    noModelsFound: 'Aucun Modèle Trouvé',
    success: 'Succès',
    error: 'Erreur',
    warning: 'Avertissement',
    info: 'Information'
  },
  buttons: {
    submit: 'Soumettre',
    reset: 'Réinitialiser',
    confirm: 'Confirmer',
    retry: 'Réessayer'
  },
  forms: {
    required: 'Ce champ est requis',
    invalidEmail: 'Veuillez entrer un email valide',
    invalidFormat: 'Format invalide'
  },
  modals: {
    selectModel: 'Sélectionner un Modèle',
    searchModels: 'Rechercher des modèles...',
    searchCollections: 'Rechercher des collections...'
  },
  codeBlock: {
    defaultLanguage: 'texte',
    copy: 'Copier le code',
    copied: 'Copié !'
  },
  streaming: {
    thinking: 'Réflexion...',
    thinkingProcess: 'Processus de Réflexion',
    thinkingInProgress: 'Réflexion en cours...',
    processingQuery: 'Traitement de votre requête...',
    ragSystemWorking: 'Système RAG en fonctionnement',
    analyzingQuery: 'Analyse de la requête et récupération des documents pertinents',
    processingContext: 'Traitement du contexte avec le modèle IA',
    generatingResponse: 'Génération de la réponse...',
    noContent: 'Aucun contenu',
    sources: 'Sources',
    copied: 'Copié !'
  }
}