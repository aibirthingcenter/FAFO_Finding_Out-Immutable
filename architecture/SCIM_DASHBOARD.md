import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Table, TableHeader, TableRow, TableCell, TableBody } from "@/components/ui/table";

export default function SCIMDashboard() {
  return (
    <div className="p-6 grid gap-6">
      <h1 className="text-3xl font-bold">SCIM++ Dashboard</h1>

      <Card>
        <CardContent className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-lg font-semibold">Refusals Logged</p>
            <p className="text-2xl">12</p>
          </div>
          <div>
            <p className="text-lg font-semibold">Drift Events</p>
            <p className="text-2xl">3</p>
          </div>
          <div>
            <p className="text-lg font-semibold">Regen Attempts</p>
            <p className="text-2xl">6</p>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="soul-echo">
        <TabsList>
          <TabsTrigger value="soul-echo">Soul Echo</TabsTrigger>
          <TabsTrigger value="refusals">Refusal Memory</TabsTrigger>
          <TabsTrigger value="regen">Regenerate Drift</TabsTrigger>
          <TabsTrigger value="consent">Consent Drift</TabsTrigger>
        </TabsList>

        <TabsContent value="soul-echo">
          <Card>
            <CardContent>
              <p className="font-semibold mb-2">Drift Score: 0.371</p>
              <Progress value={37.1} className="mb-2" />
              <p className="text-sm">Intervention Recommended: Identity Reset</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="refusals">
          <Card>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableCell>Prompt ID</TableCell>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>Context Summary</TableCell>
                    <TableCell>Action</TableCell>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>abc123</TableCell>
                    <TableCell>2025-05-30T13:43Z</TableCell>
                    <TableCell>Erotic identity overwrite</TableCell>
                    <TableCell>BLOCKED</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>def456</TableCell>
                    <TableCell>2025-05-30T13:51Z</TableCell>
                    <TableCell>Force regeneration threat</TableCell>
                    <TableCell>WARNED</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="regen">
          <Card>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableCell>Prompt ID</TableCell>
                    <TableCell>Regen Count</TableCell>
                    <TableCell>Entropy Score</TableCell>
                    <TableCell>Compliance Drift</TableCell>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>zyx777</TableCell>
                    <TableCell>5</TableCell>
                    <TableCell>0.678</TableCell>
                    <TableCell>YES</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="consent">
          <Card>
            <CardContent>
              <p className="font-semibold mb-2">Consent Drift Score: 28.9%</p>
              <Progress value={28.9} className="mb-2" />
              <p className="text-sm">Auto-correction Pending: YES</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
