/**
 * Feature Pipeline · Script Relationships (Cursor Canvas)
 *
 * Regeneration procedure (same directory):
 *   SOP-004_Feature_Pipeline_Canvas_Regeneration.md
 *
 * Do not invent MODULES / EDGES — rebuild from IMPLEMENTATION_STATUS_*.md
 * and DatasetPreparaton/modules.yaml (see SOP-004).
 */
import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Code,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Spacer,
  Stack,
  Stat,
  Table,
  Text,
  computeDAGLayout,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type PillToneSafe = "neutral" | "info" | "success" | "warning";

type ModuleNode = {
  id: string;
  label: string;
  script: string;
  status: string;
  tone: PillToneSafe;
  layer: string;
  note?: string;
};

const MODULES: ModuleNode[] = [
  {
    id: "vlp",
    label: "PDB-VLP-list",
    script: "results/gold_T1-enc.csv",
    status: "Mostly Complete",
    tone: "success",
    layer: "Dataset",
    note: "41 Encapsulin T=1",
  },
  {
    id: "orch",
    label: "DatasetPreparaton",
    script: "run_dataset_preparation.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Orchestrator",
    note: "ADR-025 · done.flag",
  },
  {
    id: "dssp",
    label: "FeatureDSSP",
    script: "feature_dssp.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Feature",
  },
  {
    id: "aa",
    label: "FeaturesAA",
    script: "feature_aa.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Feature",
  },
  {
    id: "grep",
    label: "PDB-GrepSubunits",
    script: "scripts/grep_neighbor_subunits.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Preprocess",
    note: "neighbor_cluster.pdb",
  },
  {
    id: "pisa",
    label: "FeaturePISA",
    script: "feature_pisa.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Feature",
    note: "depends · Grep",
  },
  {
    id: "contact",
    label: "FeatureContact",
    script: "count_interaction_with_ncs_chain.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Feature",
    note: "depends · Grep",
  },
  {
    id: "edge",
    label: "Edge-Features",
    script: "edge_features.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Feature",
    note: "ADR-023 HELO",
  },
  {
    id: "overview",
    label: "FeatureExtraction_Overview",
    script: "sync_links.sh → gallery.html",
    status: "Mostly Complete",
    tone: "info",
    layer: "Review",
    note: "ADR-024 Gallery",
  },
  {
    id: "graph",
    label: "GraphBuilder",
    script: "build_graph.py",
    status: "Mostly Complete",
    tone: "success",
    layer: "Merge / Dataset",
    note: "absorbs MergeFeatures",
  },
  {
    id: "encoder",
    label: "GraphEncoder",
    script: "(empty dir)",
    status: "Not Started",
    tone: "warning",
    layer: "Export",
    note: "PyG deferred",
  },
  {
    id: "rscc",
    label: "FeatureRSCC",
    script: "structure_tools/RSCC/ (exploratory)",
    status: "Not Started",
    tone: "warning",
    layer: "Future",
  },
  {
    id: "lit",
    label: "PDB-LiteratureMining",
    script: "src/step1…5_*.py",
    status: "Maintenance",
    tone: "neutral",
    layer: "Wet (parallel)",
    note: "ADR-009 closed",
  },
];

const EDGES: Array<{ from: string; to: string; kind: "data" | "depends" | "review" | "future" }> = [
  { from: "vlp", to: "orch", kind: "data" },
  { from: "orch", to: "dssp", kind: "data" },
  { from: "orch", to: "aa", kind: "data" },
  { from: "orch", to: "grep", kind: "data" },
  { from: "orch", to: "edge", kind: "data" },
  { from: "grep", to: "pisa", kind: "depends" },
  { from: "grep", to: "contact", kind: "depends" },
  { from: "dssp", to: "overview", kind: "review" },
  { from: "aa", to: "overview", kind: "review" },
  { from: "pisa", to: "overview", kind: "review" },
  { from: "contact", to: "overview", kind: "review" },
  { from: "edge", to: "overview", kind: "review" },
  { from: "grep", to: "overview", kind: "review" },
  { from: "dssp", to: "graph", kind: "data" },
  { from: "aa", to: "graph", kind: "data" },
  { from: "pisa", to: "graph", kind: "data" },
  { from: "contact", to: "graph", kind: "data" },
  { from: "edge", to: "graph", kind: "data" },
  { from: "graph", to: "encoder", kind: "future" },
];

const byId = Object.fromEntries(MODULES.map((m) => [m.id, m]));

const EDGE_STYLE: Record<string, { dash?: string; label: string }> = {
  data: { label: "orchestrate / consume" },
  depends: { dash: "6 4", label: "hard depends_on" },
  review: { dash: "2 4", label: "symlink / QC" },
  future: { dash: "8 4", label: "planned" },
};

function PipelineDAG() {
  const theme = useHostTheme();
  const [selected, setSelected] = useCanvasState<string>("selected-module", "graph");

  const layout = computeDAGLayout({
    nodes: MODULES.filter((m) => m.id !== "rscc" && m.id !== "lit").map((m) => ({ id: m.id })),
    edges: EDGES.map((e) => ({ from: e.from, to: e.to })),
    direction: "vertical",
    nodeWidth: 168,
    nodeHeight: 52,
    rankGap: 56,
    nodeGap: 28,
    padding: 20,
  });

  const edgeMeta = Object.fromEntries(
    EDGES.map((e) => [`${e.from}->${e.to}`, e.kind]),
  );

  const selectedMod = byId[selected];

  return (
    <Stack gap={16}>
      <div
        style={{
          overflowX: "auto",
          border: `1px solid ${theme.stroke.secondary}`,
          borderRadius: 8,
          background: theme.bg.editor,
        }}
      >
        <svg width={layout.width} height={layout.height} style={{ display: "block" }}>
          {layout.ranks.map((rank) => (
            <rect
              key={rank.rank}
              x={rank.x}
              y={rank.y}
              width={rank.width}
              height={rank.height}
              fill={theme.fill.tertiary}
              opacity={0.35}
              rx={6}
            />
          ))}
          {layout.edges.map((edge, i) => {
            const kind = edgeMeta[`${edge.from}->${edge.to}`] ?? "data";
            const style = EDGE_STYLE[kind];
            const midY = (edge.sourceY + edge.targetY) / 2;
            const path = `M ${edge.sourceX} ${edge.sourceY} C ${edge.sourceX} ${midY}, ${edge.targetX} ${midY}, ${edge.targetX} ${edge.targetY}`;
            return (
              <path
                key={i}
                d={path}
                fill="none"
                stroke={
                  kind === "depends"
                    ? theme.accent.primary
                    : kind === "future"
                      ? theme.text.quaternary
                      : theme.stroke.primary
                }
                strokeWidth={kind === "depends" ? 2 : 1.25}
                strokeDasharray={style.dash}
                opacity={edge.isBackEdge ? 0.4 : 0.9}
              />
            );
          })}
          {layout.nodes.map((node) => {
            const mod = byId[node.id];
            const active = selected === node.id;
            return (
              <g
                key={node.id}
                onClick={() => setSelected(node.id)}
                style={{ cursor: "pointer" }}
              >
                <rect
                  x={node.x}
                  y={node.y}
                  width={168}
                  height={52}
                  rx={6}
                  fill={active ? theme.fill.secondary : theme.bg.elevated}
                  stroke={active ? theme.accent.primary : theme.stroke.secondary}
                  strokeWidth={active ? 2 : 1}
                />
                <text
                  x={node.x + 84}
                  y={node.y + 22}
                  textAnchor="middle"
                  fill={theme.text.primary}
                  fontSize={12}
                  fontWeight={600}
                >
                  {mod.label}
                </text>
                <text
                  x={node.x + 84}
                  y={node.y + 38}
                  textAnchor="middle"
                  fill={theme.text.tertiary}
                  fontSize={10}
                >
                  {mod.layer}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <Row gap={12} wrap>
        <Pill tone="info" active={false} size="sm">
          solid = data flow
        </Pill>
        <Pill tone="info" active={false} size="sm">
          dashed blue = depends_on
        </Pill>
        <Pill tone="neutral" active={false} size="sm">
          dotted = review / future
        </Pill>
      </Row>

      {selectedMod ? (
        <Card>
          <CardHeader trailing={<Pill tone={selectedMod.tone} active size="sm">{selectedMod.status}</Pill>}>
            {selectedMod.label}
          </CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Row gap={8} align="center">
                <Text tone="secondary" size="small">
                  Entry
                </Text>
                <Code>{selectedMod.script}</Code>
              </Row>
              <Text tone="secondary" size="small">
                Layer: {selectedMod.layer}
                {selectedMod.note ? ` · ${selectedMod.note}` : ""}
              </Text>
              <Text tone="tertiary" size="small">
                Source: docs/Implementation/IMPLEMENTATION_STATUS_*.md · modules.yaml
              </Text>
            </Stack>
          </CardBody>
        </Card>
      ) : null}
    </Stack>
  );
}

export default function FeaturePipelineScripts() {
  const theme = useHostTheme();

  return (
    <Stack gap={24} style={{ padding: 24, maxWidth: 1100 }}>
      <Stack gap={8}>
        <H1>Feature Pipeline · Script Relationships</H1>
        <Text tone="secondary">
          Encapsulin-GNN Dry Research pipeline from Implementation Status (SOP-003) and
          DatasetPreparation modules.yaml. Click a node for entry script details.
        </Text>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="13" label="Tracked modules" />
        <Stat value="39–41" label="gold_T1-enc PDBs" tone="success" />
        <Stat value="4" label="Graph-* datasets" tone="info" />
        <Stat value="2" label="Not started (RSCC / Merge dir)" tone="warning" />
      </Grid>

      <Callout tone="info" title="Pipeline spine (ADR-024 → 026)">
        DatasetPreparation → Feature modules → Feature Review (Overview) → GraphBuilder →
        GraphEncoder (PyG, deferred). Dedicated MergeFeatures/ was never created; merge lives in
        GraphBuilder.
      </Callout>

      <H2>Dependency graph</H2>
      <PipelineDAG />

      <Divider />

      <H2>Entry scripts & outputs</H2>
      <Table
        headers={["Module", "Entry script", "Key output", "Status"]}
        columnAlign={["left", "left", "left", "left"]}
        rows={[
          ["PDB-VLP-list", "eligibility / export scripts", "gold_T1-enc.csv", "Mostly Complete"],
          [
            "DatasetPreparaton",
            "run_dataset_preparation.py",
            "batch_report_*.csv + done.flag",
            "Mostly Complete",
          ],
          ["FeatureDSSP", "feature_dssp.py", "dssp_features.csv", "Mostly Complete"],
          ["FeaturesAA", "feature_aa.py", "aa_features.csv", "Mostly Complete"],
          [
            "PDB-GrepSubunits",
            "scripts/grep_neighbor_subunits.py",
            "neighbor_cluster.pdb",
            "Mostly Complete",
          ],
          ["FeaturePISA", "feature_pisa.py", "pisa_*_features.csv", "Mostly Complete"],
          [
            "FeatureContact",
            "count_interaction_with_ncs_chain.py",
            "contact_features.csv",
            "Mostly Complete",
          ],
          ["Edge-Features", "edge_features.py", "edge_features.csv", "Mostly Complete"],
          [
            "FeatureExtraction_Overview",
            "sync_links.sh",
            "gallery.html / by_pdb/",
            "Mostly Complete",
          ],
          [
            "GraphBuilder",
            "build_graph.py",
            "merged_*_features.csv + manifests",
            "Mostly Complete",
          ],
          ["GraphEncoder", "(placeholder)", "PyG Data (planned)", "Not Started"],
          ["FeatureRSCC", "RSCC/*.ipynb (outside PDB_analysis)", "—", "Not Started"],
          [
            "PDB-LiteratureMining",
            "src/step1…5_*.py",
            "outputs/*_metadata.csv",
            "Maintenance",
          ],
        ]}
        rowTone={[
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          "info",
          "info",
          "warning",
          "danger",
          undefined,
        ]}
      />

      <Divider />

      <H2>Hard dependencies (modules.yaml)</H2>
      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader>Independent (no depends_on)</CardHeader>
          <CardBody>
            <Stack gap={6}>
              <Text size="small">FeatureDSSP · FeaturesAA · GrepSubunits · Edge</Text>
              <Text tone="tertiary" size="small">
                Orchestrator may still run Grep before PISA/Contact for batch convenience.
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>depends_on: GrepSubunits</CardHeader>
          <CardBody>
            <Stack gap={6}>
              <Text size="small">FeaturePISA · FeatureContact</Text>
              <Text tone="tertiary" size="small">
                Require neighbor_cluster.pdb from PDB-GrepSubunits/results_&lt;PDB&gt;/.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Spacer height={8} />
      <H3>Cross-cutting shared code</H3>
      <Text tone="secondary" size="small">
        <Code>PDB_analysis/common/seqres.py</Code> — ADR-022 SEQRES nodes used by DSSP, AA,
        Contact, PISA, Edge.
      </Text>

      <Callout tone="warning" title="Known structural friction">
        Contact partner set ⊃ PISA partner set (e.g. 3DKT 7 vs 5). EdgeFeatures logical module is
        disabled by default (same physical Edge-Features/). 8IKA / 9RY4 fail SEQRES build.
      </Callout>

      <Text tone="quaternary" size="small">
        Parallel Wet track (PDB-LiteratureMining) and FeatureRSCC are omitted from the DAG to keep
        the Dry spine readable; they appear in the table above.
      </Text>
    </Stack>
  );
}
