erDiagram
    USERS ||--o{ PROJECTS : "owns"
    USERS ||--o{ CREATOR_DNA_PROFILES : "has"
    USERS ||--o{ FEEDBACK : "provides"
    USERS ||--o{ AUDIENCE_AVATARS : "defines"
    USERS ||--o{ SUPPORTING_MATERIALS : "owns"
    USERS ||--o{ PROJECT_SETTINGS_TEMPLATES : "creates"
    USERS ||--o| BACKGROUND_JOBS : "initiates"
    USERS ||--o{ RETRIEVABLE_TEXT : "owns_source_of"
    USERS ||--o{ DNA_DETAILED_ANALYSIS : "analyzed_for"
    USERS ||--o| EVALUATION_RESULTS : "evaluates (opt)"

    PROJECTS ||--o{ CONTENT_SOURCES : "uses"
    PROJECTS ||--o{ SCRIPT_SECTIONS : "contains"
    PROJECTS ||--o{ RESEARCH_ANALYSIS : "has"
    PROJECTS ||--o{ FEEDBACK : "relates_to"
    PROJECTS ||--o{ RETRIEVABLE_TEXT : "contains"
    PROJECTS ||--o{ DNA_DETAILED_ANALYSIS : "analyzed_for"
    PROJECTS ||--o| BACKGROUND_JOBS : "relates_to"
    PROJECTS ||--o{ PROJECT_TOPICS : "defines_outline"
    PROJECTS ||--o{ GENERATED_STRUCTURES : "has_options_for"
    PROJECTS }o--|| PROJECT_AUDIENCE_AVATARS : "uses"
    PROJECTS }|..|| EDUCATIONAL_FRAMEWORKS : "uses (opt)"
    PROJECTS ||--|{ PROJECT_SETTINGS : "has_settings_for"
    PROJECTS ||--o{ PROJECT_IDEA_VALIDATION : "has_validation_for"
    PROJECTS }o..|| CREATOR_DNA_PROFILES : "uses_active_profile (opt)"
    PROJECTS ||--o{ EVALUATION_RESULTS : "evaluated_for"

    AUDIENCE_AVATARS ||--o{ PROJECT_AUDIENCE_AVATARS : "used_in"
    AUDIENCE_AVATARS ||--o{ EVALUATION_RESULTS : "is_evaluated (opt)"

    PROJECT_TOPICS ||--o{ PROJECT_TOPIC_MATERIALS : "uses"
    PROJECT_TOPICS ||--o{ EVALUATION_RESULTS : "is_evaluated (opt)"

    SUPPORTING_MATERIALS ||--o{ PROJECT_TOPIC_MATERIALS : "used_for"
    SUPPORTING_MATERIALS ||--o{ EVALUATION_RESULTS : "is_evaluated (opt)"

    CONTENT_SOURCES ||--o{ RETRIEVABLE_TEXT : "is_chunked_into"
    CONTENT_SOURCES ||--o{ DNA_DETAILED_ANALYSIS : "is_analyzed_into"

    SCRIPT_SECTIONS ||--o| RETRIEVABLE_TEXT : "is_chunked_into (opt)"
    SCRIPT_SECTIONS ||--o| SCRIPT_SECTIONS : "parent_of (opt)"
    SCRIPT_SECTIONS ||--o{ SAFETY_ANALYSIS : "has"
    SCRIPT_SECTIONS ||--o{ EVALUATION_RESULTS : "is_evaluated (opt)"
    SCRIPT_SECTIONS }o..|| GENERATED_STRUCTURES : "derived_from (opt)"
    SCRIPT_SECTIONS ||--o| BACKGROUND_JOBS : "created_by (opt)"


    GENERATED_STRUCTURES ||--o| BACKGROUND_JOBS : "created_by (opt)"
    GENERATED_STRUCTURES ||--o{ EVALUATION_RESULTS : "is_evaluated (opt)"

    DNA_DETAILED_ANALYSIS ||--o| BACKGROUND_JOBS : "created_by (opt)"

    RESEARCH_ANALYSIS ||--o| BACKGROUND_JOBS : "created_by (opt)"

    SAFETY_ANALYSIS ||--o| BACKGROUND_JOBS : "created_by (opt)"

    RETRIEVABLE_TEXT ||--o| BACKGROUND_JOBS : "created_by (opt)"

    PROJECT_SETTINGS_TEMPLATES ||--o{ PROJECT_SETTINGS : "is_template_for (opt)"

    PROJECT_IDEA_VALIDATION ||--o| BACKGROUND_JOBS : "created_by (opt)"


    USERS {
        UUID id PK
        VARCHAR email
        TIMESTAMPTZ created_at
    }

    PROJECTS {
        UUID id PK
        UUID user_id FK
        UUID selected_structure_id FK "nullable, -> GENERATED_STRUCTURES.id"
        UUID educational_framework_id FK "nullable, -> EDUCATIONAL_FRAMEWORKS.id"
        UUID active_dna_profile_id FK "nullable, -> CREATOR_DNA_PROFILES.id"
        VARCHAR title
        VARCHAR status "e.g. active, archived"
        TEXT creative_brief "nullable"
        TIMESTAMPTZ created_at
    }

    PROJECT_SETTINGS_TEMPLATES {
        UUID id PK
        UUID user_id FK
        VARCHAR template_name UK
        JSONB settings_data
        TIMESTAMPTZ created_at
    }

    PROJECT_SETTINGS {
        UUID id PK
        UUID project_id FK "Unique"
        UUID template_id FK "nullable, -> PROJECT_SETTINGS_TEMPLATES.id"
        JSONB setting_overrides
        TIMESTAMPTZ created_at
        TIMESTAMPTZ updated_at
    }

    AUDIENCE_AVATARS {
        UUID id PK
        UUID user_id FK
        VARCHAR name
        TEXT description
        JSONB details
        TIMESTAMPTZ created_at
    }

    PROJECT_AUDIENCE_AVATARS {
        UUID project_id FK
        UUID audience_avatar_id FK
    }

    SUPPORTING_MATERIALS {
        UUID id PK
        UUID user_id FK
        VARCHAR material_type
        VARCHAR uri "nullable"
        TEXT content "nullable"
        TEXT description
        JSONB metadata
        TIMESTAMPTZ created_at
    }

    PROJECT_TOPICS {
        UUID id PK
        UUID project_id FK
        TEXT topic_title
        VARCHAR selection_status "e.g. suggested, selected, rejected"
        INTEGER sequence_order
        UUID parent_topic_id FK "nullable, -> self"
        TIMESTAMPTZ created_at
    }

    PROJECT_TOPIC_MATERIALS {
        UUID project_topic_id FK
        UUID supporting_material_id FK
    }

    GENERATED_STRUCTURES {
        UUID id PK
        UUID project_id FK
        UUID initiating_job_id FK "nullable"
        JSONB structure_data
        VARCHAR status
        TIMESTAMPTZ created_at
    }

    EDUCATIONAL_FRAMEWORKS {
        UUID id PK
        VARCHAR name
        JSONB structure_template
        TEXT description
    }

    RETRIEVABLE_TEXT {
        UUID id PK
        UUID content_source_id FK "nullable"
        UUID script_section_id FK "nullable"
        UUID initiating_job_id FK "nullable"
        UUID project_id FK
        UUID user_id FK
        TEXT chunk_text
        JSONB basic_metadata "Incl. origin_type='story'/'transcript'/etc"
        VECTOR embedding "HNSW Index"
        TIMESTAMPTZ created_at
    }

    DNA_DETAILED_ANALYSIS {
        UUID id PK
        UUID content_source_id FK
        UUID initiating_job_id FK "nullable"
        UUID project_id FK
        UUID user_id FK
        JSONB pacing_stats
        JSONB keyword_analysis
        TIMESTAMPTZ created_at
    }

    CONTENT_SOURCES {
        UUID id PK
        UUID project_id FK
        VARCHAR source_type
        VARCHAR uri
        TEXT raw_transcript
        VARCHAR processing_status
        TIMESTAMPTZ created_at
        TIMESTAMPTZ updated_at
    }

    SCRIPT_SECTIONS {
        UUID id PK
        UUID project_id FK
        UUID generated_structure_id FK "nullable"
        VARCHAR section_type
        INTEGER sequence_order
        UUID parent_section_id FK "nullable"
        TEXT content "Current version"
        TEXT previous_content "nullable, Previous version"
        JSONB generation_metadata "nullable"
        JSONB hook_options "nullable"
        UUID initiating_job_id FK "nullable"
        TIMESTAMPTZ created_at
        TIMESTAMPTZ updated_at
    }

    RESEARCH_ANALYSIS {
       UUID id PK
       UUID project_id FK
       UUID initiating_job_id FK "nullable"
       JSONB key_findings
       JSONB entity_relations
       JSONB source_evaluations
       TIMESTAMPTZ created_at
    }

    SAFETY_ANALYSIS {
       UUID id PK
       UUID script_section_id FK
       UUID initiating_job_id FK "nullable"
       VARCHAR status
       JSONB details
       TIMESTAMPTZ review_timestamp
    }

    FEEDBACK {
        UUID id PK
        UUID project_id FK
        UUID user_id FK
        VARCHAR target_entity_type
        UUID target_entity_id
        TEXT feedback_content
        TIMESTAMPTZ created_at
    }

    CREATOR_DNA_PROFILES {
        UUID id PK
        UUID user_id FK
        VARCHAR profile_name
        JSONB style_notes
        JSONB fine_tuning_controls
        UUID[] source_content_ids
        TIMESTAMPTZ created_at
        TIMESTAMPTZ updated_at
    }

    BACKGROUND_JOBS {
        UUID id PK
        VARCHAR job_id UK
        VARCHAR task_name
        UUID project_id FK "nullable"
        UUID user_id FK "nullable"
        VARCHAR status
        JSONB result
        TEXT error_message
        TIMESTAMPTZ created_at
        TIMESTAMPTZ started_at
        TIMESTAMPTZ completed_at
    }

    PROJECT_IDEA_VALIDATION {
       UUID id PK
       UUID project_id FK
       UUID initiating_job_id FK "nullable"
       JSONB validation_results
       TIMESTAMPTZ created_at
    }

    EVALUATION_RESULTS {
        UUID id PK
        UUID project_id FK
        UUID evaluating_user_id FK "nullable"
        VARCHAR target_entity_type
        UUID target_entity_id
        VARCHAR evaluator_type "AI or USER"
        VARCHAR metric_name
        FLOAT score "nullable"
        JSONB details "nullable"
        TIMESTAMPTZ created_at
    }
