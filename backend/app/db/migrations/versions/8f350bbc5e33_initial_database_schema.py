"""Initial database schema

Revision ID: 8f350bbc5e33
Revises:
Create Date: 2025-04-16 08:41:16.210504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector

# revision identifiers, used by Alembic.
revision: str = "8f350bbc5e33"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable the pgvector extension first
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # === PHASE 1: Create all tables first without foreign key constraints ===

    # Create users table
    op.create_table(
        "users",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    # Create projects table
    op.create_table(
        "projects",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("selected_structure_id", sa.UUID(), nullable=True),
        sa.Column("educational_framework_id", sa.UUID(), nullable=True),
        sa.Column("active_dna_profile_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("creative_brief", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_projects_active_dna_profile_id"),
        "projects",
        ["active_dna_profile_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_projects_created_at"), "projects", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_projects_educational_framework_id"),
        "projects",
        ["educational_framework_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_projects_selected_structure_id"),
        "projects",
        ["selected_structure_id"],
        unique=False,
    )
    op.create_index(op.f("ix_projects_status"), "projects", ["status"], unique=False)
    op.create_index(
        op.f("ix_projects_updated_at"), "projects", ["updated_at"], unique=False
    )
    op.create_index(op.f("ix_projects_user_id"), "projects", ["user_id"], unique=False)

    # Create background_jobs table
    op.create_table(
        "background_jobs",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("job_id", sa.String(), nullable=False),
        sa.Column("task_name", sa.String(), nullable=False),
        sa.Column("project_id", sa.UUID(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("result", postgresql.JSONB(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_background_jobs_completed_at"),
        "background_jobs",
        ["completed_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_background_jobs_created_at"),
        "background_jobs",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_background_jobs_job_id"), "background_jobs", ["job_id"], unique=True
    )
    op.create_index(
        op.f("ix_background_jobs_project_id"),
        "background_jobs",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_background_jobs_started_at"),
        "background_jobs",
        ["started_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_background_jobs_status"), "background_jobs", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_background_jobs_task_name"),
        "background_jobs",
        ["task_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_background_jobs_user_id"), "background_jobs", ["user_id"], unique=False
    )

    # Create creator_dna_profiles table
    op.create_table(
        "creator_dna_profiles",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("profile_name", sa.String(), nullable=False),
        sa.Column("style_notes", postgresql.JSONB(), nullable=False),
        sa.Column(
            "fine_tuning_controls",
            postgresql.JSONB(),
            nullable=False,
        ),
        sa.Column("source_content_ids", postgresql.ARRAY(sa.UUID()), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_creator_dna_profiles_created_at"),
        "creator_dna_profiles",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_creator_dna_profiles_source_content_ids"),
        "creator_dna_profiles",
        ["source_content_ids"],
        unique=False,
    )
    op.create_index(
        op.f("ix_creator_dna_profiles_updated_at"),
        "creator_dna_profiles",
        ["updated_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_creator_dna_profiles_user_id"),
        "creator_dna_profiles",
        ["user_id"],
        unique=False,
    )

    # Create audience_avatars table
    op.create_table(
        "audience_avatars",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audience_avatars_created_at"),
        "audience_avatars",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audience_avatars_user_id"),
        "audience_avatars",
        ["user_id"],
        unique=False,
    )

    # Create project_audience_avatars join table
    op.create_table(
        "project_audience_avatars",
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("audience_avatar_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("project_id", "audience_avatar_id"),
    )
    op.create_index(
        op.f("ix_project_audience_avatars_audience_avatar_id"),
        "project_audience_avatars",
        ["audience_avatar_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_audience_avatars_project_id"),
        "project_audience_avatars",
        ["project_id"],
        unique=False,
    )

    # Create educational_frameworks table
    op.create_table(
        "educational_frameworks",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "structure_template",
            postgresql.JSONB(),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create generated_structures table
    op.create_table(
        "generated_structures",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column("structure_data", postgresql.JSONB(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_generated_structures_initiating_job_id"),
        "generated_structures",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_generated_structures_project_id"),
        "generated_structures",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_generated_structures_status"),
        "generated_structures",
        ["status"],
        unique=False,
    )

    # Create script_sections table
    op.create_table(
        "script_sections",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("generated_structure_id", sa.UUID(), nullable=True),
        sa.Column("section_type", sa.String(), nullable=False),
        sa.Column("sequence_order", sa.Integer(), nullable=False),
        sa.Column("parent_section_id", sa.UUID(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("previous_content", sa.Text(), nullable=True),
        sa.Column(
            "generation_metadata",
            postgresql.JSONB(),
            nullable=True,
        ),
        sa.Column("hook_options", postgresql.JSONB(), nullable=True),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_script_sections_created_at"),
        "script_sections",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_generated_structure_id"),
        "script_sections",
        ["generated_structure_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_initiating_job_id"),
        "script_sections",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_parent_section_id"),
        "script_sections",
        ["parent_section_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_project_id"),
        "script_sections",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_section_type"),
        "script_sections",
        ["section_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_sequence_order"),
        "script_sections",
        ["sequence_order"],
        unique=False,
    )
    op.create_index(
        op.f("ix_script_sections_updated_at"),
        "script_sections",
        ["updated_at"],
        unique=False,
    )

    # Create safety_analyses table
    op.create_table(
        "safety_analyses",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("script_section_id", sa.UUID(), nullable=False),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("details", postgresql.JSONB(), nullable=False),
        sa.Column("review_timestamp", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_safety_analyses_initiating_job_id"),
        "safety_analyses",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_safety_analyses_script_section_id"),
        "safety_analyses",
        ["script_section_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_safety_analyses_status"), "safety_analyses", ["status"], unique=False
    )

    # Create content_sources table
    op.create_table(
        "content_sources",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("uri", sa.String(), nullable=False),
        sa.Column("raw_transcript", sa.Text(), nullable=False),
        sa.Column("processing_status", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_content_sources_created_at"),
        "content_sources",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_content_sources_processing_status"),
        "content_sources",
        ["processing_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_content_sources_project_id"),
        "content_sources",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_content_sources_updated_at"),
        "content_sources",
        ["updated_at"],
        unique=False,
    )

    # Create dna_detailed_analyses table
    op.create_table(
        "dna_detailed_analyses",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("content_source_id", sa.UUID(), nullable=False),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("pacing_stats", postgresql.JSONB(), nullable=False),
        sa.Column(
            "keyword_analysis", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_dna_detailed_analyses_content_source_id"),
        "dna_detailed_analyses",
        ["content_source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dna_detailed_analyses_initiating_job_id"),
        "dna_detailed_analyses",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dna_detailed_analyses_project_id"),
        "dna_detailed_analyses",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_dna_detailed_analyses_user_id"),
        "dna_detailed_analyses",
        ["user_id"],
        unique=False,
    )

    # Create project_settings_templates table
    op.create_table(
        "project_settings_templates",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("template_name", sa.String(), nullable=False),
        sa.Column(
            "settings_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "template_name", name="uq_user_template_name"),
    )
    op.create_index(
        op.f("ix_project_settings_templates_created_at"),
        "project_settings_templates",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_settings_templates_user_id"),
        "project_settings_templates",
        ["user_id"],
        unique=False,
    )

    # Create project_settings table
    op.create_table(
        "project_settings",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("template_id", sa.UUID(), nullable=True),
        sa.Column(
            "setting_overrides", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            onupdate=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_project_settings_created_at"),
        "project_settings",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_settings_project_id"),
        "project_settings",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_settings_template_id"),
        "project_settings",
        ["template_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_settings_updated_at"),
        "project_settings",
        ["updated_at"],
        unique=False,
    )

    # Create project_topics table
    op.create_table(
        "project_topics",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("topic_title", sa.Text(), nullable=False),
        sa.Column("selection_status", sa.String(), nullable=False),
        sa.Column("sequence_order", sa.Integer(), nullable=False),
        sa.Column("parent_topic_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_project_topics_parent_topic_id"),
        "project_topics",
        ["parent_topic_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_topics_project_id"),
        "project_topics",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_topics_selection_status"),
        "project_topics",
        ["selection_status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_topics_sequence_order"),
        "project_topics",
        ["sequence_order"],
        unique=False,
    )

    # Create supporting_materials table
    op.create_table(
        "supporting_materials",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("material_type", sa.String(), nullable=False),
        sa.Column("uri", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "material_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_supporting_materials_created_at"),
        "supporting_materials",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_supporting_materials_user_id"),
        "supporting_materials",
        ["user_id"],
        unique=False,
    )

    # Create project_topic_materials join table
    op.create_table(
        "project_topic_materials",
        sa.Column("project_topic_id", sa.UUID(), nullable=False),
        sa.Column("supporting_material_id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("project_topic_id", "supporting_material_id"),
    )
    op.create_index(
        op.f("ix_project_topic_materials_project_topic_id"),
        "project_topic_materials",
        ["project_topic_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_topic_materials_supporting_material_id"),
        "project_topic_materials",
        ["supporting_material_id"],
        unique=False,
    )

    # Create research_analyses table
    op.create_table(
        "research_analyses",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column(
            "key_findings", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "entity_relations", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column(
            "source_evaluations",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_research_analyses_initiating_job_id"),
        "research_analyses",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_research_analyses_project_id"),
        "research_analyses",
        ["project_id"],
        unique=False,
    )

    # Create project_idea_validations table
    op.create_table(
        "project_idea_validations",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column(
            "validation_results",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_project_idea_validations_initiating_job_id"),
        "project_idea_validations",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_idea_validations_project_id"),
        "project_idea_validations",
        ["project_id"],
        unique=False,
    )

    # Create feedback table
    op.create_table(
        "feedback",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("target_entity_type", sa.String(), nullable=False),
        sa.Column("target_entity_id", sa.UUID(), nullable=False),
        sa.Column("feedback_content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_feedback_project_id"), "feedback", ["project_id"], unique=False
    )
    op.create_index(
        op.f("ix_feedback_target_entity_id"),
        "feedback",
        ["target_entity_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_feedback_target_entity_type"),
        "feedback",
        ["target_entity_type"],
        unique=False,
    )
    op.create_index(op.f("ix_feedback_user_id"), "feedback", ["user_id"], unique=False)

    # Create evaluation_results table
    op.create_table(
        "evaluation_results",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("evaluating_user_id", sa.UUID(), nullable=True),
        sa.Column("target_entity_type", sa.String(), nullable=False),
        sa.Column("target_entity_id", sa.UUID(), nullable=False),
        sa.Column("evaluator_type", sa.String(), nullable=False),
        sa.Column("metric_name", sa.String(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_evaluation_results_evaluating_user_id"),
        "evaluation_results",
        ["evaluating_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_metric_name"),
        "evaluation_results",
        ["metric_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_project_id"),
        "evaluation_results",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_target_entity_id"),
        "evaluation_results",
        ["target_entity_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_target_entity_type"),
        "evaluation_results",
        ["target_entity_type"],
        unique=False,
    )

    # Create retrievable_text table with pgvector support
    op.create_table(
        "retrievable_text",
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("content_source_id", sa.UUID(), nullable=True),
        sa.Column("script_section_id", sa.UUID(), nullable=True),
        sa.Column("initiating_job_id", sa.UUID(), nullable=True),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("basic_metadata", postgresql.JSONB(), nullable=False),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(1536), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_retrievable_text_content_source_id"),
        "retrievable_text",
        ["content_source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_retrievable_text_initiating_job_id"),
        "retrievable_text",
        ["initiating_job_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_retrievable_text_project_id"),
        "retrievable_text",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_retrievable_text_script_section_id"),
        "retrievable_text",
        ["script_section_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_retrievable_text_user_id"),
        "retrievable_text",
        ["user_id"],
        unique=False,
    )
    # Create a standard vector index instead of HNSW
    op.execute(
        "CREATE INDEX ix_retrievable_text_embedding ON retrievable_text USING ivfflat (embedding vector_l2_ops)"
    )

    # === PHASE 2: Add all foreign key constraints ===

    # Add foreign keys for users relationships
    op.create_foreign_key(
        "fk_creator_dna_profiles_user_id",
        "creator_dna_profiles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_audience_avatars_user_id",
        "audience_avatars",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_project_settings_templates_user_id",
        "project_settings_templates",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_supporting_materials_user_id",
        "supporting_materials",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_feedback_user_id",
        "feedback",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_evaluation_results_evaluating_user_id",
        "evaluation_results",
        "users",
        ["evaluating_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_background_jobs_user_id",
        "background_jobs",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_dna_detailed_analyses_user_id",
        "dna_detailed_analyses",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_retrievable_text_user_id",
        "retrievable_text",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Add foreign keys for projects relationships
    op.create_foreign_key(
        "fk_projects_user_id",
        "projects",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_projects_educational_framework_id",
        "projects",
        "educational_frameworks",
        ["educational_framework_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_projects_active_dna_profile_id",
        "projects",
        "creator_dna_profiles",
        ["active_dna_profile_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_projects_selected_structure_id",
        "projects",
        "generated_structures",
        ["selected_structure_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_foreign_key(
        "fk_content_sources_project_id",
        "content_sources",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_script_sections_project_id",
        "script_sections",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_research_analyses_project_id",
        "research_analyses",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_feedback_project_id",
        "feedback",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_project_topics_project_id",
        "project_topics",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_generated_structures_project_id",
        "generated_structures",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_project_settings_project_id",
        "project_settings",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_project_idea_validations_project_id",
        "project_idea_validations",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_dna_detailed_analyses_project_id",
        "dna_detailed_analyses",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_evaluation_results_project_id",
        "evaluation_results",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_retrievable_text_project_id",
        "retrievable_text",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_background_jobs_project_id",
        "background_jobs",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Add foreign keys for project_audience_avatars (m2m) relationships
    op.create_foreign_key(
        "fk_project_audience_avatars_project_id",
        "project_audience_avatars",
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_project_audience_avatars_avatar_id",
        "project_audience_avatars",
        "audience_avatars",
        ["audience_avatar_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Add foreign keys for background_jobs relationships with job-created entities
    op.create_foreign_key(
        "fk_generated_structures_job_id",
        "generated_structures",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_script_sections_job_id",
        "script_sections",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_dna_detailed_analyses_job_id",
        "dna_detailed_analyses",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_research_analyses_job_id",
        "research_analyses",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_safety_analyses_job_id",
        "safety_analyses",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_retrievable_text_job_id",
        "retrievable_text",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_project_idea_validations_job_id",
        "project_idea_validations",
        "background_jobs",
        ["initiating_job_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Add foreign keys for content_sources relationships
    op.create_foreign_key(
        "fk_dna_detailed_analyses_content_id",
        "dna_detailed_analyses",
        "content_sources",
        ["content_source_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_retrievable_text_content_id",
        "retrievable_text",
        "content_sources",
        ["content_source_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Add foreign keys for script_sections relationships
    op.create_foreign_key(
        "fk_script_sections_parent_id",
        "script_sections",
        "script_sections",
        ["parent_section_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_script_sections_structure_id",
        "script_sections",
        "generated_structures",
        ["generated_structure_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_safety_analyses_section_id",
        "safety_analyses",
        "script_sections",
        ["script_section_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_retrievable_text_section_id",
        "retrievable_text",
        "script_sections",
        ["script_section_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Add foreign keys for project_settings relationships
    op.create_foreign_key(
        "fk_project_settings_template_id",
        "project_settings",
        "project_settings_templates",
        ["template_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Add foreign keys for project_topics relationships
    op.create_foreign_key(
        "fk_project_topics_parent_id",
        "project_topics",
        "project_topics",
        ["parent_topic_id"],
        ["id"],
        ondelete="SET NULL",
    )

    # Add foreign keys for project_topic_materials (m2m) relationships
    op.create_foreign_key(
        "fk_topic_materials_topic_id",
        "project_topic_materials",
        "project_topics",
        ["project_topic_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_topic_materials_material_id",
        "project_topic_materials",
        "supporting_materials",
        ["supporting_material_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Drop all foreign key constraints first
    # This order is the reverse of the upgrade() function, dropping child tables before parent tables

    # Drop all foreign keys first
    op.drop_constraint(
        "fk_topic_materials_material_id", "project_topic_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_topic_materials_topic_id", "project_topic_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_project_topics_parent_id", "project_topics", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_project_settings_template_id", "project_settings", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_retrievable_text_section_id", "retrievable_text", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_safety_analyses_section_id", "safety_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_script_sections_structure_id", "script_sections", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_script_sections_parent_id", "script_sections", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_retrievable_text_content_id", "retrievable_text", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_dna_detailed_analyses_content_id",
        "dna_detailed_analyses",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_project_idea_validations_job_id",
        "project_idea_validations",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_retrievable_text_job_id", "retrievable_text", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_safety_analyses_job_id", "safety_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_research_analyses_job_id", "research_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_dna_detailed_analyses_job_id", "dna_detailed_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_script_sections_job_id", "script_sections", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_generated_structures_job_id", "generated_structures", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_project_audience_avatars_avatar_id",
        "project_audience_avatars",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_project_audience_avatars_project_id",
        "project_audience_avatars",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_background_jobs_project_id", "background_jobs", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_retrievable_text_project_id", "retrievable_text", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_evaluation_results_project_id", "evaluation_results", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_dna_detailed_analyses_project_id",
        "dna_detailed_analyses",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_project_idea_validations_project_id",
        "project_idea_validations",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_project_settings_project_id", "project_settings", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_generated_structures_project_id", "generated_structures", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_project_topics_project_id", "project_topics", type_="foreignkey"
    )
    op.drop_constraint("fk_feedback_project_id", "feedback", type_="foreignkey")
    op.drop_constraint(
        "fk_research_analyses_project_id", "research_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_script_sections_project_id", "script_sections", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_content_sources_project_id", "content_sources", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_projects_selected_structure_id", "projects", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_projects_active_dna_profile_id", "projects", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_projects_educational_framework_id", "projects", type_="foreignkey"
    )
    op.drop_constraint("fk_projects_user_id", "projects", type_="foreignkey")
    op.drop_constraint(
        "fk_retrievable_text_user_id", "retrievable_text", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_dna_detailed_analyses_user_id", "dna_detailed_analyses", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_background_jobs_user_id", "background_jobs", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_evaluation_results_evaluating_user_id",
        "evaluation_results",
        type_="foreignkey",
    )
    op.drop_constraint("fk_feedback_user_id", "feedback", type_="foreignkey")
    op.drop_constraint(
        "fk_supporting_materials_user_id", "supporting_materials", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_project_settings_templates_user_id",
        "project_settings_templates",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_audience_avatars_user_id", "audience_avatars", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_creator_dna_profiles_user_id", "creator_dna_profiles", type_="foreignkey"
    )

    # Now drop all tables in reverse order
    op.drop_table("retrievable_text")
    op.drop_table("evaluation_results")
    op.drop_table("feedback")
    op.drop_table("project_idea_validations")
    op.drop_table("research_analyses")
    op.drop_table("project_topic_materials")
    op.drop_table("supporting_materials")
    op.drop_table("project_topics")
    op.drop_table("project_settings")
    op.drop_table("project_settings_templates")
    op.drop_table("dna_detailed_analyses")
    op.drop_table("content_sources")
    op.drop_table("safety_analyses")
    op.drop_table("script_sections")
    op.drop_table("generated_structures")
    op.drop_table("educational_frameworks")
    op.drop_table("project_audience_avatars")
    op.drop_table("audience_avatars")
    op.drop_table("creator_dna_profiles")
    op.drop_table("background_jobs")
    op.drop_table("projects")
    op.drop_table("users")

    # Drop the pgvector extension at the end
    op.execute("DROP EXTENSION IF EXISTS vector")
